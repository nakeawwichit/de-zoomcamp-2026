import pandas as pd
import os
import glob

def convert_parquet_to_csv():
    # Find all parquet files in the current directory
    parquet_files = glob.glob("*.parquet")
    
    if not parquet_files:
        print("No .parquet files found in the current directory.")
        return

    print(f"Found {len(parquet_files)} parquet files. Starting conversion...")

    for parquet_file in parquet_files:
        try:
            # Construct output filename
            csv_file = parquet_file.replace(".parquet", ".csv")
            
            print(f"Converting '{parquet_file}' to '{csv_file}'...")
            
            # Read the parquet file
            df = pd.read_parquet(parquet_file)
            
            # Save as CSV
            df.to_csv(csv_file, index=False)
            
            print(f"Successfully converted '{parquet_file}'")
            
        except Exception as e:
            print(f"Error converting '{parquet_file}': {e}")

if __name__ == "__main__":
    convert_parquet_to_csv()
