import pandas as pd
from sqlalchemy import create_engine
import urllib

# Connection details
server = 'localhost,1433'
database = 'industrial_bi_db'
username = 'sa'
password = 'YourStrongP@ss123'  # match your actual Docker password

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"TrustServerCertificate=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Load each CSV into its matching staging table
tables = {
    "data/machines.csv": "stg_machines",
    "data/production.csv": "stg_production",
    "data/sales.csv": "stg_sales",
    "data/budget.csv": "stg_finance"
}

for csv_file, table_name in tables.items():
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"✅ Loaded {len(df)} rows into {table_name}")

print("\n🎉 All data loaded successfully!")