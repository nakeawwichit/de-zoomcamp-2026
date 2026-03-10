### Data Engineering Zoomcamp 2026 - Week 5 Homework

This repository contains the solution for the Week 6 homework of the Data Engineering Zoomcamp 2026. The task involves processing New York Yellow Taxi trip data from November 2025 using Apache Spark.

### Environment Setup

To keep the local machine clean, Apache Spark is run inside a Docker container using the following image: `jupyter/pyspark-notebook:spark-3.5.0`.

### Prerequisite

- Docker & Docker Compose

### How to Run

1. Start the Spark environment:
   ```bash
   docker compose up -d
   ```
2. Run the solution script:
   ```bash
   docker compose exec spark /usr/local/spark/bin/spark-submit work/solution.py
   ```

### Question 1: Spark Version

**Answer**: `3.5.0`

### Question 2: Yellow November 2025 Partition Size

The dataset was repartitioned into 4 files.
**Average Size**: `24.40 MB` (Closest option: **25MB**)

### Question 3: Count Records

Total taxi trips on November 15th, 2025.
**Answer**: `162,604`

### Question 4: Longest Trip Duration

The longest trip in hours.
**Answer**: `90.65 hours`

### Question 5: User Interface Port

The default port for the Spark Web UI.
**Answer**: `4040`

### Question 6: Least Frequent Pickup Location Zone

The zone with the fewest pickups.
**Answer**: `Governor's Island/Ellis Island/Liberty Island` (1 trip)

---

_Note: The script outputs logs to [output_nov_2025.txt](output_nov_2025.txt)._
