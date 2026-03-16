# Sales Data — Exploratory Data Analysis & Visualization

## Overview
End-to-end Sales Data Analysis (520 rows, 15 columns) from a Senior Data Scientist perspective.  
Covers data profiling, quality checks, cleaning, feature engineering, business insights, and visualizations.

---

## Project Structure
```
Sales-EDA/
│
├── sales_data.csv              # Raw input data
├── sales_data_clean.csv        # Cleaned output (auto-generated)
├── phase1_sales_eda.py         # Phase 1 — EDA & Cleaning
├── phase2_sales_viz.py         # Phase 2 — Visualizations
├── plots/                      # All saved charts
│   ├── chart1_monthly_revenue_trend.png
│   ├── chart1_monthly_revenue_trend_interactive.html
│   ├── chart2_top_products_revenue.png
│   ├── chart2_top_products_revenue_interactive.html
│   ├── chart3_revenue_by_region.png
│   ├── chart3_revenue_by_region_interactive.html
│   ├── chart4_sales_rep_leaderboard.png
│   ├── chart4_sales_rep_leaderboard_interactive.html
│   ├── chart5_return_rate_by_product.png
│   ├── chart5_return_rate_by_product_interactive.html
│   ├── chart6_channel_mix.png
│   └── chart6_channel_mix_interactive.html
└── README.md
```

---

## Phase 1 — EDA & Cleaning

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
- Cleaned data saved as `sales_data_clean.csv` in the same folder

---

## Phase 2 — Visualizations

Both **static (Matplotlib + Seaborn)** and **interactive (Plotly)** charts generated for:

| # | Chart | Type |
|---|-------|------|
| 1 | Monthly Revenue Trend | Line chart |
| 2 | Top 10 Products by Revenue | Bar chart |
| 3 | Revenue by Region | Bar + Pie chart |
| 4 | Sales Rep Leaderboard | Bar chart |
| 5 | Return Rate by Product | Bar chart |
| 6 | Channel Mix | Bar + Pie chart |

All charts saved to `plots/` folder as `.png` (static) and `.html` (interactive).

---

## Setup & Usage

### 1. Activate your environment
```bash
conda activate myenv
```

### 2. Install dependencies
```bash
pip install numpy pandas matplotlib seaborn plotly
```

### 3. Run Phase 1 — EDA
```bash
python phase1_sales_eda.py
```

### 4. Run Phase 2 — Visualizations
```bash
python phase2_sales_viz.py
```

---

## Requirements
| Package    | Version |
|------------|---------|
| Python     | 3.13+   |
| pandas     | latest  |
| numpy      | latest  |
| matplotlib | latest  |
| seaborn    | latest  |
| plotly     | latest  |

---

## Author
Japendra  
Data Analysis Portfolio — Sales EDA Project