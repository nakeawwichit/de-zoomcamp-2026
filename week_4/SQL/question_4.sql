SELECT 
    pickup_zone,
    SUM(revenue_monthly_total_amount) as total_revenue
FROM `<project_id>.trips_data_all.fct_monthly_zone_revenue`
WHERE 
    service_type = 'Green' 
    AND year = 2020
GROUP BY 1
ORDER BY total_revenue DESC
LIMIT 5;