"""
Phase 1: Exploratory Data Analysis — Sales Data
Approach: Senior Lead / Data Scientist perspective
Dataset: sales_data.csv (520 rows, 15 columns)
"""

import numpy as np
import pandas as pd
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", 20)
pd.set_option("display.float_format", "{:.2f}".format)

# ─────────────────────────────────────────────────────────────────
# 1. LOAD & FIRST LOOK
# ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1 — LOAD & FIRST LOOK")
print("=" * 60)

df = pd.read_csv("sales_data.csv")
print(f"Shape: {df.shape}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")

# ─────────────────────────────────────────────────────────────────
# 2. AUTOMATED DATA PROFILE (reusable function)
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2 — AUTOMATED DATA PROFILE")
print("=" * 60)

def profile_dataframe(df, name="DataFrame"):
    """
    Senior-level data profiler.
    Prints nulls, uniqueness, types, sample values.
    Returns a summary DataFrame for further analysis.
    """
    profile = []
    for col in df.columns:
        n_total   = len(df)
        n_null    = df[col].isnull().sum()
        n_unique  = df[col].nunique()
        dtype     = df[col].dtype
        pct_null  = round(n_null / n_total * 100, 2)
        pct_unique= round(n_unique / n_total * 100, 2)
        sample    = str(df[col].dropna().unique()[:3].tolist())
        profile.append({
            "column":   col,
            "dtype":    str(dtype),
            "nulls":    n_null,
            "null_%":   pct_null,
            "unique":   n_unique,
            "unique_%": pct_unique,
            "sample":   sample[:60]
        })

    result = pd.DataFrame(profile)
    print(f"\n{'─'*60}")
    print(f"PROFILE: {name}  |  {df.shape[0]} rows × {df.shape[1]} cols")
    print(f"{'─'*60}")
    print(result.to_string(index=False))
    return result

profile = profile_dataframe(df, "Sales")

# ─────────────────────────────────────────────────────────────────
# 3. DETECT & HANDLE DATA QUALITY ISSUES
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3 — DATA QUALITY ISSUES")
print("=" * 60)

issues = []

# Duplicate check
dupes = df.duplicated(subset="order_id").sum()
print(f"Duplicate order_ids: {dupes}")
issues.append(f"Duplicates: {dupes}")

# Negative / zero values that should be positive
neg_qty   = (df["quantity"] <= 0).sum()
zero_price= (df["unit_price"] == 0).sum()
print(f"Negative quantity rows: {neg_qty}")
print(f"Zero unit_price rows:   {zero_price}")

# Value distribution of key categoricals
print(f"\nRegion value counts (including bad data):\n{df['region'].value_counts(dropna=False)}")
print(f"\nReturned value counts:\n{df['returned'].value_counts(dropna=False)}")

# ─── Clean ───────────────────────────────────────────────────────
df_clean = df.copy()
df_clean = df_clean.drop_duplicates(subset="order_id", keep="first")
df_clean = df_clean[df_clean["quantity"] > 0]
df_clean = df_clean[df_clean["unit_price"] > 0]
df_clean["region"]   = df_clean["region"].replace("UNKNOWN", np.nan).fillna("Unknown")
df_clean["returned"] = df_clean["returned"].fillna(False)
df_clean["discount_pct"] = df_clean["discount_pct"].fillna(0)
df_clean["unit_price"] = df_clean.groupby("product")["unit_price"].transform(
    lambda x: x.fillna(x.median())
)

# ─── Feature engineering ─────────────────────────────────────────
df_clean["order_date"] = pd.to_datetime(df_clean["order_date"])
df_clean["ship_date"]  = pd.to_datetime(df_clean["ship_date"])
df_clean["ship_days"]  = (df_clean["ship_date"] - df_clean["order_date"]).dt.days
df_clean["revenue"]    = df_clean["quantity"] * df_clean["unit_price"] * (1 - df_clean["discount_pct"] / 100)
df_clean["month"]      = df_clean["order_date"].dt.to_period("M")
df_clean["quarter"]    = df_clean["order_date"].dt.to_period("Q")

print(f"\nClean shape: {df_clean.shape}")
print(f"Remaining nulls:\n{df_clean.isnull().sum()[df_clean.isnull().sum() > 0]}")

# ─────────────────────────────────────────────────────────────────
# EXPORT CLEAN DATA — same folder as script
# ─────────────────────────────────────────────────────────────────
output_path = Path(__file__).parent / "sales_data_clean.csv"
df_clean.to_csv(output_path, index=False)
print(f"\n✓ Clean data saved → {output_path}  ({df_clean.shape[0]} rows × {df_clean.shape[1]} cols)")

# ─────────────────────────────────────────────────────────────────
# 4. BUSINESS INSIGHTS — WHAT A LEAD WANTS TO KNOW
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4 — BUSINESS INSIGHTS")
print("=" * 60)

# Revenue summary
total_rev = df_clean["revenue"].sum()
print(f"\nTotal Revenue:   ${total_rev:,.0f}")
print(f"Avg Order Value: ${df_clean['revenue'].mean():,.0f}")
print(f"Median Order:    ${df_clean['revenue'].median():,.0f}")

# Top 3 products by revenue
print("\nTop 5 Products by Revenue:")
print(
    df_clean.groupby("product")["revenue"]
    .agg(["sum","mean","count"])
    .rename(columns={"sum":"total_rev","mean":"avg_rev","count":"orders"})
    .sort_values("total_rev", ascending=False)
    .head(5)
)

# Region performance
print("\nRevenue by Region:")
region_rev = df_clean.groupby("region")["revenue"].agg(["sum","count"]).rename(
    columns={"sum":"revenue","count":"orders"})
region_rev["avg_order"] = (region_rev["revenue"] / region_rev["orders"]).round(2)
region_rev["rev_share_%"] = (region_rev["revenue"] / region_rev["revenue"].sum() * 100).round(2)
print(region_rev.sort_values("revenue", ascending=False))

# Return rate by product
print("\nReturn Rate by Product (%):")
print(
    df_clean.groupby("product")["returned"]
    .apply(lambda x: pd.to_numeric(x, errors="coerce").mean() * 100)
    .round(2)
    .sort_values(ascending=False)
)

# Monthly revenue trend
print("\nMonthly Revenue (first 6 months):")
monthly = df_clean.groupby("month")["revenue"].sum().head(6)
for period, rev in monthly.items():
    bar = "█" * int(rev / total_rev * 100)
    print(f"  {period}  ${rev:>10,.0f}  {bar}")

# Sales rep performance
print("\nSales Rep Leaderboard:")
print(
    df_clean.groupby("sales_rep")["revenue"]
    .agg(["sum","count","mean"])
    .rename(columns={"sum":"total","count":"orders","mean":"avg_per_order"})
    .sort_values("total", ascending=False)
)

# Channel mix
print("\nRevenue by Channel:")
print(df_clean.groupby("channel")["revenue"].sum().sort_values(ascending=False))

print("\n✓ Phase 1 complete. Clean data ready for visualization.")