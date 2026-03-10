import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os

# Question 1: Spark Version
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('homework') \
    .getOrCreate()

print(f"Question 1: Spark version is {spark.version}")

# Question 2: Yellow November 2025
# Read the parquet file
df_yellow = spark.read.parquet("work/yellow_tripdata_2025-11.parquet")

# Repartition to 4 and save
df_yellow.repartition(4).write.parquet("work/temp_yellow_2025_11", mode='overwrite')

# Calculate average size
import glob
files = glob.glob("work/temp_yellow_2025_11/*.parquet")
total_size = sum(os.path.getsize(f) for f in files)
avg_size = total_size / len(files) / (1024 * 1024)
print(f"Question 2: Average size of Parquet files is {avg_size:.2f} MB")

# Question 3: Count records on Nov 15th
count_nov_15 = df_yellow.filter(F.to_date(df_yellow.tpep_pickup_datetime) == '2025-11-15').count()
print(f"Question 3: Trips on November 15th: {count_nov_15}")

# Question 4: Longest trip in hours
df_duration = df_yellow.withColumn('duration_hours', 
    (F.unix_timestamp('tpep_dropoff_datetime') - F.unix_timestamp('tpep_pickup_datetime')) / 3600)

max_duration = df_duration.select(F.max('duration_hours')).collect()[0][0]
print(f"Question 4: Longest trip duration: {max_duration:.2f} hours")

# Question 5: Spark UI port
print("Question 5: Spark UI port is 4040")

# Question 6: Least frequent pickup location zone
df_zones = spark.read \
    .option("header", "true") \
    .csv("work/taxi_zone_lookup.csv")

# Join and group by zone
df_joined = df_yellow.join(df_zones, df_yellow.PULocationID == df_zones.LocationID)
least_frequent = df_joined.groupBy('Zone') \
    .count() \
    .orderBy('count', ascending=True) \
    .first()

print(f"Question 6: Least frequent pickup location zone: {least_frequent['Zone']} with {least_frequent['count']} trips")

spark.stop()
