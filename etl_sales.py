import pandas as pd
from sqlalchemy import create_engine

# 1. Read CSV
df = pd.read_csv("sales_data_sample.csv", encoding="latin1")

# 2. Cleaning / derived fields
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
df = df.dropna(subset=['ORDERNUMBER', 'CUSTOMERNAME', 'COUNTRY', 'SALES', 'ORDERDATE'])

df['ORDER_YEAR'] = df['ORDERDATE'].dt.year
df['ORDER_MONTH'] = df['ORDERDATE'].dt.month

# ensure numeric
df['SALES'] = pd.to_numeric(df['SALES'], errors='coerce')
df['QUANTITYORDERED'] = pd.to_numeric(df['QUANTITYORDERED'], errors='coerce')
# Data quality checks (simple prints/logs)
total_rows = len(df)
missing_sales = df['SALES'].isna().sum()
negative_sales = (df['SALES'] < 0).sum()
negative_qty = (df['QUANTITYORDERED'] < 0).sum()

print(f"Total rows after cleaning: {total_rows}")
print(f"Rows with missing SALES: {missing_sales}")
print(f"Rows with negative SALES: {negative_sales}")
print(f"Rows with negative QUANTITYORDERED: {negative_qty}")

# Optional: drop negative values if any
df = df[df['SALES'] >= 0]
df = df[df['QUANTITYORDERED'] >= 0]


# 3. Example aggregation: sales by country & year
sales_country_year = df.groupby(['COUNTRY', 'ORDER_YEAR'])['SALES'].agg(
    total_sales='sum',
    order_count='count',
    avg_order_value='mean'
).reset_index()

# 4. Connect to MySQL  ← change user/password if needed
engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/sales_etl_db")

# 5. Load into MySQL
sales_country_year.to_sql("sales_country_year", engine, if_exists="replace", index=False)
# Sales by PRODUCTLINE and year
sales_productline_year = df.groupby(['PRODUCTLINE', 'ORDER_YEAR'])['SALES'].agg(
    total_sales='sum',
    order_count='count',
    avg_order_value='mean'
).reset_index()

sales_productline_year.to_sql("sales_productline_year", engine, if_exists="replace", index=False)

# Sales by DEALSIZE and year
sales_dealsize_year = df.groupby(['DEALSIZE', 'ORDER_YEAR'])['SALES'].agg(
    total_sales='sum',
    order_count='count',
    avg_order_value='mean'
).reset_index()

sales_dealsize_year.to_sql("sales_dealsize_year", engine, if_exists="replace", index=False)

# Total sales per customer
customer_sales = df.groupby('CUSTOMERNAME')['SALES'].agg(
    total_sales='sum',
    order_count='count'
).reset_index()

customer_sales = customer_sales.sort_values('total_sales', ascending=False)
top_10_customers = customer_sales.head(10)

top_10_customers.to_sql("top_10_customers", engine, if_exists="replace", index=False)

# Top customers per country (top 5)
customer_country_sales = df.groupby(['COUNTRY', 'CUSTOMERNAME'])['SALES'].agg(
    total_sales='sum'
).reset_index()

customer_country_sales['rank_in_country'] = customer_country_sales.groupby('COUNTRY')['total_sales'] \
    .rank(method='first', ascending=False)

top_customers_country = customer_country_sales[customer_country_sales['rank_in_country'] <= 5]

top_customers_country.to_sql("top_customers_country", engine, if_exists="replace", index=False)


print("ETL to MySQL finished successfully!")
