# Cloud-Native Data Engineering Pipeline on AWS (S3 → RDS PostgreSQL)

## Overview
- This project demonstrates a cloud-native data engineering pipeline built on AWS.  
- It ingests raw JSON data from Amazon S3, applies transformations using Python, and loads the processed data into Amazon RDS (PostgreSQL).  
- CloudWatch is used for centralized logging and observability.

## Architecture
S3 (Raw JSON) → Python ETL → Amazon RDS (PostgreSQL)  
CloudWatch Logs for monitoring ETL execution
```
                 ┌──────────────────────┐
                 │   Amazon S3           │
                 │  (Raw JSON Data)      │
                 └──────────┬───────────┘
                            │
                            │ boto3
                            ▼
                 ┌──────────────────────┐
                 │  Python ETL Pipeline │
                 │  (Extract & Transform│
                 │   using pandas)      │
                 └──────────┬───────────┘
                            │
                            │ SQL Inserts
                            ▼
                 ┌──────────────────────┐
                 │ Amazon RDS            │
                 │ PostgreSQL            │
                 │ (Structured Storage) │
                 └──────────┬───────────┘
                            │
                            │ Execution Logs
                            ▼
                 ┌──────────────────────┐
                 │ Amazon CloudWatch     │
                 │ (ETL Monitoring)     │
                 └──────────────────────┘

```

## Tech Stack
- AWS S3
- AWS RDS (PostgreSQL)
- AWS CloudWatch
- Python (boto3, pandas, psycopg2)
- Git & GitHub

## Project Structure
```
aws_sales_etl_cloud/
├── read_s3_json.py # Extract data from S3
├── transform_data.py # Data transformation logic
├── load_to_rds.py # Load data into PostgreSQL (RDS)
├── cloudwatch_logger.py # CloudWatch logging utility
├── sales_data.json # Sample raw JSON data
├── rds_setup.py # RDS connection & setup
└── README.md
```

## Data Flow
1. Raw JSON data is stored in an S3 bucket
2. Data is read using boto3
3. Transformations are applied using pandas
4. Cleaned data is loaded into PostgreSQL on AWS RDS
5. ETL execution logs are pushed to CloudWatch

## Key Learnings
- Designing cloud-native ETL pipelines
- Working with AWS managed services (S3, RDS, CloudWatch)
- Secure credential management using IAM
- Writing production-style Python ETL code
- Version control using Git and GitHub

## Future Improvements
- Automate pipeline using AWS Lambda or Airflow
- Add data quality checks
- Implement CI/CD for ETL jobs
