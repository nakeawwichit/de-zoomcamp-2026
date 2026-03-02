### Data Engineering Zoomcamp 2026 - Week 5 Homework

#### Project Structure

- dez-pipeline/ - Bruin pipeline project for NYC taxi data
  - .bruin.yml - Environment and DuckDB connection configuration
  - pipeline/pipeline.yml - Pipeline name, schedule, variables
  - pipeline/assets/ingestion/ - Raw data ingestion (Python + CSV seed)
  - pipeline/assets/staging/ - Data cleaning, deduplication, JOIN
  - pipeline/assets/reports/ - Aggregated reporting layer

#### Question 1: Bruin Pipeline Structure

Answer: `.bruin.yml` and `pipeline.yml` (assets can be anywhere)

#### Question 2: Materialization Strategies

Answer: `time_interval` - incremental based on a time column

#### Question 3: Pipeline Variables

```bash
bruin run --var 'taxi_types=["yellow"]'
```

Answer: `bruin run --var 'taxi_types=["yellow"]'`

#### Question 4: Running with Dependencies

```bash
bruin run ingestion/trips.py --downstream
```

Answer: `bruin run ingestion/trips.py --downstream`

#### Question 5: Quality Checks

```yaml
checks:
  - name: not_null
```

Answer: `name: not_null`

#### Question 6: Lineage and Dependencies

```bash
bruin lineage <path>
```

Answer: `bruin lineage`

#### Question 7: First-Time Run

```bash
bruin run ./pipeline/pipeline.yml --full-refresh
```

Answer: `--full-refresh`
