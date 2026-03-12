import pandas as pd
import mysql.connector

# 1. Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",          # change if your user is different
    password="your password",
    database="sales_etl_db"
)

tables = [
    "sales_country_year",
    "sales_productline_year",
    "sales_dealsize_year",
    "top_10_customers",
    "top_customers_country"
]

for table in tables:
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    csv_filename = f"{table}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Exported {table} to {csv_filename}")

conn.close()
