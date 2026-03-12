# Sales Data Engineering Project – ETL to MySQL and AWS S3

Small end-to-end ETL pipeline built on a sample sales dataset using Python, MySQL, and Amazon S3. The project follows a data lake style with separate `raw/` and `transformed/` layers in S3. [web:187][web:191][web:192][web:293]

## Architecture

**Goal:** Extract raw sales data, transform it into analytics-ready tables, load into MySQL, and store both raw and transformed datasets in Amazon S3. [web:187][web:191][web:192]

High-level flow:

1. **Extract**
   - Input: Raw CSV file `sales_data_sample.csv`.
   - Read into Pandas for processing. [web:201][web:220][web:227]

2. **Transform** (Python + Pandas)
   Implemented in `etl_sales.py`:
   - Clean and prepare the raw dataset.
   - Create multiple aggregated tables:
     - `sales_country_year` – sales aggregated by country and year.
     - `sales_productline_year` – sales aggregated by product line and year.
     - `sales_dealsize_year` – sales aggregated by deal size and year.
     - `top_10_customers` – top 10 customers by total sales.
     - `top_customers_country` – top customers per country by revenue. [web:201][web:203]

3. **Load**
   - Load transformed tables into a MySQL database: `sales_etl_db`.
   - Export each transformed table from MySQL back to CSV using `export_transformed_to_csv.py`. [web:220][web:224][web:227]
   - Upload CSVs to an Amazon S3 bucket with a logical structure:
     - `raw/sales_data_sample.csv`
     - `transformed/sales_country_year.csv`
     - `transformed/sales_productline_year.csv`
     - `transformed/sales_dealsize_year.csv`
     - `transformed/top_10_customers.csv`
     - `transformed/top_customers_country.csv` [web:191][web:192][web:215]

## Tech Stack

- **Language:** Python (Pandas)
- **Database:** MySQL (`sales_etl_db`)
- **Cloud Storage:** Amazon S3 (data lake-style layout)
- **Libraries:** `pandas`, `mysql-connector-python`
- **Tools:** AWS Management Console, MySQL Workbench / CLI, Git & GitHub [web:287][web:290][web:293]

## Dataset

- Source: Sample sales dataset (orders, customers, product lines, deal size, revenue). [web:286][web:290]
- Format: CSV
- Example fields: `ORDERNUMBER`, `ORDERDATE`, `COUNTRY`, `CUSTOMERNAME`, `PRODUCTLINE`, `DEALSIZE`, `SALES`, etc.
- The full raw dataset may not be included in this repo; optionally, a small anonymized sample can be placed in `data/`. [web:286][web:287][web:290]

> Note: All credentials (MySQL, AWS) are removed from the code. Use your own local environment variables or config files when running the project. [web:281][web:285][web:291]

## ETL Steps in Detail

### 1. Extract

- Read `sales_data_sample.csv` into a Pandas DataFrame.
- Basic cleaning: type conversions, handling missing values where needed. [web:201][web:203][web:220]

### 2. Transform

In `etl_sales.py`:

- Create `sales_country_year`:
  - Group by `COUNTRY` and `YEAR(ORDERDATE)`, aggregate `SALES`.  

- Create `sales_productline_year`:
  - Group by `PRODUCTLINE` and year, aggregate `SALES`.  

- Create `sales_dealsize_year`:
  - Group by `DEALSIZE` and year, aggregate `SALES`.  

- Create `top_10_customers`:
  - Rank customers by total `SALES`, select top 10.  

- Create `top_customers_country`:
  - For each `COUNTRY`, rank customers by revenue. [web:187][web:201][web:203]

### 3. Load

- Connect to MySQL and create database `sales_etl_db`.
- Write each DataFrame as a table in MySQL. [web:222][web:225]
- In `export_transformed_to_csv.py`, use SQL queries + Pandas to export each table:
  - `sales_country_year.csv`
  - `sales_productline_year.csv`
  - `sales_dealsize_year.csv`
  - `top_10_customers.csv`
  - `top_customers_country.csv` [web:220][web:224][web:227]
- Upload the raw and transformed CSVs to S3:
  - `raw/` for original file.
  - `transformed/` for all derived tables. [web:191][web:192][web:215][web:274]

## Repository Structure

```text
data-engineering-project/
├── etl_sales.py                   # Main ETL: raw CSV -> transformed tables -> MySQL
├── export_transformed_to_csv.py   # Export MySQL tables -> CSV files
├── data/
│   └── sample_sales_data_sample.csv   # Optional small sample of raw data (for demo)
├── README.md
└── requirements.txt               # Python dependencies
