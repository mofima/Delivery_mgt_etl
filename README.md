# 📦 AppSheet + Python + PostgreSQL Order Tracking Pipeline

From **chaos to clarity** — this project shows how I helped a small delivery business modernize their order tracking using **AppSheet**, **Python (gspread + pandas)**, **PostgreSQL**, and **Power BI**.

> 💡 Built entirely with free tools and runs on a basic Windows laptop.

---

## 📘 Project Overview

The business initially relied on a messy Google Sheet to track orders, vendors, and expenses. As daily volumes grew, it became unmanageable.

### ✅ The Solution
I designed a lightweight but scalable system that:
- Uses **AppSheet** as a mobile data entry front-end.
- Extracts data from **Google Sheets** with Python.
- Cleans and loads it into a local **PostgreSQL** database.
- Connects **Power BI** for fully automated reporting.

---

## 🗂️ Data Model & AppSheet Setup

Before any coding, I designed a simple **ERD** to represent the core business entities:
- Orders
- Vendors
- Expenses
- Employees

### AppSheet Features
The AppSheet app was built to:
- 📋 Add & View Daily Orders
- 💸 Log Daily Expenses
- 🧾 Manage Vendors
- 📊 Display Revenue Charts (e.g., by Vendor)

AppSheet directly syncs with Google Sheets — making it easy for staff to enter data from phones or browsers.

---

## 🔄 ETL Pipeline: Google Sheets ➜ PostgreSQL

### 🔧 Tools Used
| Tool         | Purpose                                  |
|--------------|-------------------------------------------|
| `gspread`    | Connects to Google Sheets API            |
| `pandas`     | Data cleaning and transformation         |
| `psycopg2`   | Load data into PostgreSQL                |
| Task Scheduler | Schedules daily ETL runs (Windows)     |

### 1. Authentication
- Enabled the Sheets API via Google Cloud.
- Created a Service Account with a JSON key.
- Shared the Google Sheet with the service email.

### 2. `extract.py`
- Connects to Google Sheets using credentials.
- Extracts records into pandas DataFrames.
- Logs errors like missing columns or API failures.

### 3. `transform.py`
- Cleans column names, formats dates, removes blanks.
- Applies transformations across all sheets.
- Uses reusable pandas functions with logging.

### 4. `load.py`
- Upserts data into PostgreSQL using `ON CONFLICT`.
- Soft-deletes missing records (`is_deleted = TRUE`).
- Reactivates records if re-added.
- Ensures referential integrity.

### 5. Scheduling
- Runs daily via **Windows Task Scheduler**.
- Ensures the DB reflects the live state of Google Sheets.
- Logging + rollback logic makes it robust.

---

## 📊 Reporting in Power BI

Power BI connects directly to PostgreSQL for live reporting.

### Sample Visuals
- 💰 Revenue by Vendor (Pie Chart)
- 🧾 Daily Order Totals
- 💼 Expense Reports
- 🧮 Profit Calculations

> Reports are always up to date — no manual refreshes needed.

---

## 🏁 Final Thoughts

This system transformed messy spreadsheets into a clean, scalable workflow that automates both data collection and reporting.

✅ No more broken formulas  
✅ No more emailing reports  
✅ Just clear, timely insights for better business decisions

---
## 🛠 Requirements

```bash
Python 3.x
gspread
pandas
psycopg2-binary
dotenv
