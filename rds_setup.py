from sqlalchemy import create_engine, text

DB_HOST = "sales-postgres-db.cxc806qa2bae.ap-south-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "salesdb"
DB_USER = "postgres"
DB_PASSWORD = "postgres123"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS sales_staging (
            order_id INT,
            order_date DATE,
            customer_id VARCHAR(50),
            product VARCHAR(100),
            category VARCHAR(50),
            quantity INT,
            unit_price NUMERIC
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS sales_audit_history (
            order_id INT,
            order_date DATE,
            customer_id VARCHAR(50),
            product VARCHAR(100),
            category VARCHAR(50),
            quantity INT,
            unit_price NUMERIC,
            load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))

print("PostgreSQL tables created successfully")
