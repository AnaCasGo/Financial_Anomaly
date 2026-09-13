import os
from pathlib import Path
import pandas as pd
from google.cloud import bigquery


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SERVICE_ACCOUNT = PROJECT_ROOT / "config" / "gcp_key.json"

# Service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(SERVICE_ACCOUNT)

PROJECT_ID = "seventh-fact-508510-d5"  # Replace with your actual GCP Project ID
DATASET_ID = "financial_anomaly"
RAW_DATA_DIR = Path("data/01_raw")

def upload_csv_to_bigquery(csv_path: Path, table_name: str, client: bigquery.Client):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    
    print(f"Uploading {csv_path.name} to BigQuery table {table_id}...")
    
    df = pd.read_csv(csv_path)
    
    # Configure load job
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, # Overwrite table if exists
        autodetect=True,
    )
    
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for job to complete
    
    print(f"Successfully loaded {len(df):,} rows into {table_id}.")

def main():
    client = bigquery.Client(project=PROJECT_ID)
    
    files_to_upload = {
        "customers.csv": "raw_customers",
        "merchants.csv": "raw_merchants",
        "transactions_historical.csv": "raw_transactions_historical",
        "transactions_production.csv": "raw_transactions_production",
    }
    
    for file_name, table_name in files_to_upload.items():
        file_path = RAW_DATA_DIR / file_name
        if file_path.exists():
            upload_csv_to_bigquery(file_path, table_name, client)
        else:
            print(f"Warning: {file_name} not found in {RAW_DATA_DIR}")

if __name__ == "__main__":
    main()