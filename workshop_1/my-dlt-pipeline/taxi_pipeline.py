"""NYC Taxi Trip Data Pipeline using dlt.

Loads paginated taxi trip data from the Data Engineering Zoomcamp API into DuckDB.
"""

import dlt
import requests


BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"


@dlt.resource(name="rides", write_disposition="replace")
def taxi_rides():
    """Fetch all pages of taxi ride data from the API."""
    page = 1
    while True:
        response = requests.get(BASE_URL, params={"page": page})
        response.raise_for_status()
        data = response.json()

        if not data:  # empty page = stop
            break

        yield data
        print(f"  Page {page}: {len(data)} records loaded")
        page += 1


if __name__ == "__main__":
    # Create the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_data",
    )

    # Run the pipeline
    load_info = pipeline.run(taxi_rides())

    # Print load info
    print(load_info)
    print(f"\nPipeline completed successfully!")
