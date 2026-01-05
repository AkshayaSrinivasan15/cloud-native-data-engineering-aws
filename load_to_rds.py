import boto3
import pandas as pd
from sqlalchemy import create_engine

# AWS
BUCKET = "cloud-json-data-raw"
KEY = "raw/sales_data.json"

# RDS
DB_HOST = "sales-postgres-db.cxc806qa2bae.ap-south-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "salesdb"
DB_USER = "postgres"
DB_PASSWORD = "postgres123"

# Read JSON from S3
s3 = boto3.client("s3")
obj = s3.get_object(Bucket=BUCKET, Key=KEY)
df = pd.read_json(obj["Body"])

# Transform
df["order_date"] = pd.to_datetime(df["order_date"])

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load staging
df.to_sql("sales_staging", engine, if_exists="replace", index=False)

# Append to audit/history
df.to_sql("sales_audit_history", engine, if_exists="append", index=False)

print("Data loaded into RDS successfully")
