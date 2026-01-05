import boto3
import json
import pandas as pd

# S3 details
BUCKET_NAME = "cloud-json-data-raw"
OBJECT_KEY = "raw/sales_data.json"

# Read JSON from S3
s3 = boto3.client("s3")
response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
content = response["Body"].read().decode("utf-8")
data = json.loads(content)

df = pd.DataFrame(data)

print("Raw data loaded")
print(df.head())

# -----------------------
# TRANSFORMATIONS
# -----------------------

# Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"])

# Create derived column
df["total_amount"] = df["quantity"] * df["unit_price"]

# Basic validation
if df.isnull().sum().any():
    raise ValueError("Null values found after transformation")

print("\nTransformed data")
print(df.head())

print("\nSchema after transformation")
print(df.dtypes)
