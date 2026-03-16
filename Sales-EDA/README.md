# Sales Data — Exploratory Data Analysis (Phase 1)

## Overview
Phase 1 EDA on a sales dataset (520 rows, 15 columns) from a Senior Data Scientist perspective.  
Covers data profiling, quality checks, cleaning, feature engineering, and business insights.

---

## Project Structure
```
Sales-EDA/
│
├── sales_data.csv           # Raw input data
├── sales_data_clean.csv     # Cleaned output (auto-generated)
├── phase1_sales_eda.py      # Main EDA script
├── plots/                   # Visualizations folder
└── README.md                # Project documentation
```

---

## What the Script Does

### Step 1 — Load & First Look
- Loads `sales_data.csv`
- Prints shape, column dtypes, and first 5 rows

### Step 2 — Automated Data Profile
- Reusable `profile_dataframe()` function
- Reports nulls, unique values, dtypes, and sample values per column

### Step 3 — Data Quality & Cleaning
- Removes duplicate `order_id` rows
- Drops rows with negative quantity or zero unit price
- Fixes `UNKNOWN` region values
- Fills nulls in `returned`, `discount_pct`, and `unit_price`

### Step 4 — Feature Engineering
- Parses `order_date` and `ship_date` to datetime
- Computes `ship_days`, `revenue`, `month`, `quarter`

### Step 5 — Business Insights
- Total revenue, avg and median order value
- Top 5 products by revenue
- Revenue by region with share %
- Return rate by product
- Monthly revenue trend
- Sales rep leaderboard
- Revenue by channel

### Export
- Cleaned data saved as `sales_data_clean.csv` in the same folder as the script

---

## Setup & Usage

### 1. Clone / open the project
```bash
cd Sales-EDA
```

### 2. Activate your environment
```bash
conda activate myenv
```

### 3. Install dependencies
```bash
pip install numpy pandas
```

### 4. Run the script
```bash
python phase1_sales_eda.py
```

---

## Requirements
| Package | Version  |
|---------|----------|
| Python  | 3.13+    |
| pandas  | latest   |
| numpy   | latest   |

---

## Output
- `sales_data_clean.csv` — cleaned and feature-engineered dataset ready for Phase 2 visualization

---

## Author
Geetu  
Data Analysis Portfolio — Sales EDA Project