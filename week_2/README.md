# Data Engineering Zoomcamp 2026 - Week 2: Workflow Orchestration (Kestra)

This folder contains the homework solutions for Week 2, focusing on Workflow Orchestration using **Kestra**.

## Project Structure

- `docker/`: Docker Compose setup for Kestra and Postgres.
- `flows/`: Kestra workflow definitions (YAML files) for each homework question.

## Usage

1. **Start Kestra:**
   ```bash
   cd docker
   docker-compose up -d
   ```
   *Access Kestra UI at [http://localhost:8080](http://localhost:8080)*

2. **Import Flows:**
   You can copy the YAML content from the `flows/` directory and create new flows in the Kestra UI.

---

## Homework Solutions

### Question 1: Uncompressed File Size
**Objective:** Find the uncompressed file size of Yellow Taxi data for `2020-12`.

- **Solution Flow:** `flows/taxi_extract_subflow.yml`
- **Method:**
  - Modified the flow to include a shell task that downloads, unzips, and checks the file size.
  - Used `wc -c` to get exact bytes and `awk` to convert to **MiB**.
- **Answer:** `128.3 MiB`

### Question 2: Variable Rendering
**Objective:** What is the rendered value of the variable `file` when inputs are `green`, `2020`, `04`?

- **Solution Flow:** `flows/debug_vars.yml` (and `question_2.yml`)
- **Method:**
  - By default, Kestra does *lazy evaluation*. To force the nested variable strings to resolve, we used the `render()` function:
    ```yaml
    {{ render(vars.file) }}
    ```
- **Answer:** `green_tripdata_2020-04.csv`

### Question 3: Yellow Taxi 2020 Row Count
**Objective:** How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

- **Solution Flow:** `flows/question_3.yml`
- **Method:**
  - Created a Python script task running in a Docker container.
  - Looped through months `01` to `12`.
  - Downloaded each file, streamed usage `gzip` to count lines efficiently without storing uncompressed data.
- **Answer:** `24,648,499`

### Question 4: Green Taxi 2020 Row Count
**Objective:** How many rows are there for the Green Taxi data for all CSV files in the year 2020?

- **Solution Flow:** `flows/question_4.yml`
- **Method:**
  - Similar Python script approach as Q3, but specific to Green Taxi URLs.
- **Answer:** `1,734,051`

### Question 5: Yellow Taxi March 2021 Row Count
**Objective:** How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

- **Solution Flow:** `flows/question_5.yml`
- **Method:**
  - Targeted download script for `yellow_tripdata_2021-03.csv.gz`.
- **Answer:** `1,925,152`

### Question 6: Timezone Configuration
**Objective:** How would you configure the timezone to New York in a Schedule trigger?

- **Solution Flow:** `flows/question_6.yml`
- **Answer:** 
  Add a timezone property set to America/New_York in the Schedule trigger configuration:
  ```yaml
  triggers:
    - id: daily_schedule
      type: io.kestra.plugin.core.trigger.Schedule
      cron: "0 9 * * *"
      timezone: "America/New_York"
  ```

---

## Troubleshooting & Notes

- **Docker Permissions:** modified `docker-compose.yml` to run Kestra as `root` user to allow access to `docker.sock`.
- **Postgres Version:** Upgraded to Postgres 16 in `docker-compose.yml`.
- **Outputs:** Kestra Download task output file size was not directly accessible in the variable context in this version, so `du` command was used.

