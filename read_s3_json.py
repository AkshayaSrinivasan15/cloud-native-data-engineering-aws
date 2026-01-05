import boto3
import json
import pandas as pd
#from datetime import datetime
from datetime import datetime, timezone


from cloudwatch_logger import create_log_stream, log_message

# -------------------
# Config
# -------------------
BUCKET_NAME = "cloud-json-data-raw"
OBJECT_KEY = "raw/sales_data.json"
LOG_GROUP = "aws-sales-etl-logs"
#LOG_STREAM = f"etl-run-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
LOG_STREAM = f"etl-run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

# -------------------
# Initialize services
# -------------------
s3 = boto3.client("s3")
create_log_stream(LOG_GROUP, LOG_STREAM)

# -------------------
# ETL Step: Extract
# -------------------
try:
    log_message(LOG_GROUP, LOG_STREAM, "Starting S3 JSON extraction")

    response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
    content = response["Body"].read().decode("utf-8")

    data = json.loads(content)
    df = pd.DataFrame(data)

    log_message(
        LOG_GROUP,
        LOG_STREAM,
        f"Successfully read {len(df)} records from S3"
    )

except Exception as e:
    log_message(
        LOG_GROUP,
        LOG_STREAM,
        f"FAILED during S3 extraction: {str(e)}"
    )
    raise

# -------------------
# Basic Validation
# -------------------
log_message(
    LOG_GROUP,
    LOG_STREAM,
    f"Schema detected: {dict(df.dtypes)}"
)

# -------------------
# Preview (local only)
# -------------------
print("Data successfully read from S3")
print(df.head())
print("\nSchema:")
print(df.dtypes)

log_message(LOG_GROUP, LOG_STREAM, "ETL extraction step completed successfully")
