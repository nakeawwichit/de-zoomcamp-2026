import os
from datetime import date, timedelta
from typing import Optional

import pandas as pd
import plotly.express as px
import streamlit as st
from google.cloud import bigquery


st.set_page_config(page_title="E-commerce Marketing Funnel", layout="wide")
st.title("E-commerce Marketing Funnel Dashboard")

project_id = os.getenv("GCP_PROJECT_ID")
mart_dataset = os.getenv("BQ_DATASET_MART", "ecom_mart")

if not project_id:
    st.error("Missing GCP_PROJECT_ID environment variable.")
    st.stop()

client = bigquery.Client(project=project_id)


def _to_date(value: object) -> Optional[date]:
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "date") and callable(value.date):
        return value.date()  # pandas Timestamp, datetime
    if isinstance(value, date):
        return value
    return None


@st.cache_data(ttl=600)
def load_order_date_bounds() -> tuple[Optional[date], Optional[date]]:
    """Olist orders are mostly 2016–2018; wide defaults like 2020–today return no rows."""
    q = f"""
    select
      min(order_date) as min_d,
      max(order_date) as max_d
    from `{project_id}.{mart_dataset}.mart_category_daily_performance`
    """
    row = client.query(q).to_dataframe().iloc[0]
    min_d = _to_date(row["min_d"])
    max_d = _to_date(row["max_d"])
    if min_d is None or max_d is None:
        return None, None
    return min_d, max_d


min_data_date, max_data_date = load_order_date_bounds()

if min_data_date is not None and max_data_date is not None:
    default_start = min_data_date
    default_end = max_data_date
else:
    default_start = date(2016, 1, 1)
    default_end = date.today()

st.sidebar.caption(
    f"Data in warehouse: **{min_data_date}** to **{max_data_date}**"
    if min_data_date and max_data_date
    else "Could not read date bounds from BigQuery."
)

end_date = st.sidebar.date_input("End date", value=default_end)
start_date = st.sidebar.date_input("Start date", value=default_start)

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

category_list_query = f"""
select distinct product_category
from `{project_id}.{mart_dataset}.mart_category_daily_performance`
where product_category is not null
order by product_category
"""
all_categories_df = client.query(category_list_query).to_dataframe()
all_categories = all_categories_df["product_category"].tolist()
selected_categories = st.sidebar.multiselect(
    "Product categories",
    options=all_categories,
    default=[],
    help="Leave empty to include all categories.",
)

category_query = f"""
select
  product_category,
  sum(revenue) as revenue
from `{project_id}.{mart_dataset}.mart_category_daily_performance`
where order_date between @start_date and @end_date
  and (@use_category_filter = false or product_category in unnest(@categories))
group by product_category
order by revenue desc
limit 15
"""

funnel_query = f"""
select
  order_date,
  sum(placed_orders) as placed_orders,
  sum(approved_orders) as approved_orders,
  sum(delivered_orders) as delivered_orders
from `{project_id}.{mart_dataset}.mart_order_lifecycle_funnel_daily`
where order_date between @start_date and @end_date
group by order_date
order by order_date
"""

category_job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date.isoformat()),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date.isoformat()),
        bigquery.ScalarQueryParameter("use_category_filter", "BOOL", len(selected_categories) > 0),
        bigquery.ArrayQueryParameter("categories", "STRING", selected_categories),
    ]
)
funnel_job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date.isoformat()),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date.isoformat()),
    ]
)

category_df = client.query(category_query, job_config=category_job_config).to_dataframe()
funnel_df = client.query(funnel_query, job_config=funnel_job_config).to_dataframe()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue Distribution by Product Category")
    if category_df.empty:
        st.info("No data for selected period.")
    else:
        fig_category = px.bar(
            category_df,
            x="product_category",
            y="revenue",
            title="Top categories by revenue",
        )
        fig_category.update_layout(xaxis_title="Category", yaxis_title="Revenue")
        st.plotly_chart(fig_category, use_container_width=True)

with col2:
    st.subheader("Daily Order Lifecycle Trend")
    if funnel_df.empty:
        st.info("No data for selected period.")
    else:
        melted = funnel_df.melt(
            id_vars=["order_date"],
            value_vars=["placed_orders", "approved_orders", "delivered_orders"],
            var_name="stage",
            value_name="orders_count",
        )
        fig_funnel = px.line(
            melted,
            x="order_date",
            y="orders_count",
            color="stage",
            title="Placed -> Approved -> Delivered",
        )
        fig_funnel.update_layout(xaxis_title="Order date", yaxis_title="Orders")
        st.plotly_chart(fig_funnel, use_container_width=True)

st.caption("Funnel definition is order lifecycle based on Olist order timestamps.")
