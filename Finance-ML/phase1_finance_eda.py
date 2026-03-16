"""
Phase 1: Exploratory Data Analysis — Finance / Loan Default Data
Approach: Senior Lead / Data Scientist perspective
Dataset: finance_data.csv (1000 rows, 20 columns)
"""

import numpy as np
import pandas as pd
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", 25)
pd.set_option("display.float_format", "{:.2f}".format)

# ─────────────────────────────────────────────────────────────────
# 1. LOAD & FIRST LOOK
# ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1 — LOAD & FIRST LOOK")
print("=" * 60)

BASE_DIR = Path(__file__).parent
df = pd.read_csv(BASE_DIR / "finance_data.csv")
print(f"Shape: {df.shape}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")

# ─────────────────────────────────────────────────────────────────
# 2. AUTOMATED DATA PROFILE
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
        n_total    = len(df)
        n_null     = df[col].isnull().sum()
        n_unique   = df[col].nunique()
        dtype      = df[col].dtype
        pct_null   = round(n_null / n_total * 100, 2)
        pct_unique = round(n_unique / n_total * 100, 2)
        sample     = str(df[col].dropna().unique()[:3].tolist())
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

profile = profile_dataframe(df, "Finance")

# ─────────────────────────────────────────────────────────────────
# 3. DETECT & HANDLE DATA QUALITY ISSUES
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3 — DATA QUALITY ISSUES")
print("=" * 60)

# Duplicate check
dupes = df.duplicated().sum()
print(f"Duplicate rows: {dupes}")

# Null summary
null_summary = df.isnull().sum()
null_summary = null_summary[null_summary > 0]
print(f"\nColumns with nulls:\n{null_summary}")

# Out-of-range checks
neg_income  = (df["income_annual"] <= 0).sum()
neg_loan    = (df["loan_amount"] <= 0).sum()
bad_credit  = ((df["credit_score"] < 300) | (df["credit_score"] > 850)).sum()
neg_age     = (df["age"] < 18).sum()
print(f"\nInvalid income rows:       {neg_income}")
print(f"Invalid loan amount rows:  {neg_loan}")
print(f"Invalid credit score rows: {bad_credit}")
print(f"Under 18 age rows:         {neg_age}")

# Key categorical distributions
print(f"\nDefaulted value counts:\n{df['defaulted'].value_counts(dropna=False)}")
print(f"\nEmployment status:\n{df['employment_status'].value_counts(dropna=False)}")
print(f"\nLoan purpose:\n{df['loan_purpose'].value_counts(dropna=False)}")
print(f"\nHome ownership:\n{df['home_ownership'].value_counts(dropna=False)}")
print(f"\nLoan grade:\n{df['loan_grade'].value_counts(dropna=False)}")

# ─── Clean ───────────────────────────────────────────────────────
df_clean = df.copy()

# Remove duplicates
df_clean = df_clean.drop_duplicates()

# Remove invalid rows
df_clean = df_clean[df_clean["income_annual"] > 0]
df_clean = df_clean[df_clean["loan_amount"] > 0]
df_clean = df_clean[df_clean["age"] >= 18]
df_clean = df_clean[df_clean["credit_score"].between(300, 850)]

# Fill numeric nulls with median
for col in ["income_annual", "credit_score", "debt_existing",
            "employment_years", "num_credit_accounts",
            "num_hard_inquiries", "late_payments_2yr", "interest_rate"]:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())

# Fill categorical nulls
for col in ["employment_status", "loan_purpose", "home_ownership",
            "loan_grade", "gender", "state"]:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].fillna("Unknown")

# ─── Feature engineering ─────────────────────────────────────────
df_clean["debt_to_income"]    = (df_clean["loan_amount"] / df_clean["income_annual"]).round(4)
df_clean["monthly_payment"]   = (df_clean["loan_amount"] / df_clean["loan_term_months"]).round(2)
df_clean["payment_to_income"] = (df_clean["monthly_payment"] / (df_clean["income_annual"] / 12)).round(4)
df_clean["total_debt_ratio"]  = ((df_clean["loan_amount"] + df_clean["debt_existing"]) / df_clean["income_annual"]).round(4)
df_clean["interest_cost_total"] = (df_clean["loan_amount"] * df_clean["interest_rate"] / 100 * df_clean["loan_term_months"] / 12).round(2)
df_clean["risk_per_year"]     = (df_clean["late_payments_2yr"] / 2.0).round(2)

df_clean["credit_tier"] = pd.cut(
    df_clean["credit_score"],
    bins=[0, 549, 649, 699, 749, 850],
    labels=["Very Poor", "Fair", "Good", "Very Good", "Excellent"]
)

df_clean["income_tier"] = pd.cut(
    df_clean["income_annual"],
    bins=[0, 30000, 60000, 100000, 200000, 99999999],
    labels=["Low", "Lower-Mid", "Mid", "Upper-Mid", "High"]
)

df_clean["loan_size"] = pd.cut(
    df_clean["loan_amount"],
    bins=[0, 5000, 15000, 30000, 99999999],
    labels=["Small", "Medium", "Large", "Very Large"]
)

print(f"\nClean shape: {df_clean.shape}")
print(f"Remaining nulls:\n{df_clean.isnull().sum()[df_clean.isnull().sum() > 0]}")

# ─────────────────────────────────────────────────────────────────
# EXPORT CLEAN DATA — same folder as script
# ─────────────────────────────────────────────────────────────────
output_path = BASE_DIR / "finance_data_clean.csv"
df_clean.to_csv(output_path, index=False)
print(f"\n✓ Clean data saved → {output_path}  ({df_clean.shape[0]} rows × {df_clean.shape[1]} cols)")

# ─────────────────────────────────────────────────────────────────
# 4. BUSINESS INSIGHTS
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4 — BUSINESS INSIGHTS")
print("=" * 60)

# ── Default Rate Overview ────────────────────────────────────────
print("\n── DEFAULT RATE OVERVIEW ──")
total        = len(df_clean)
total_default= df_clean["defaulted"].sum()
default_rate = df_clean["defaulted"].mean() * 100
print(f"Total Loans:       {total:,}")
print(f"Total Defaults:    {total_default:,}")
print(f"Overall Default Rate: {default_rate:.1f}%")

# ── Borrower Demographics ────────────────────────────────────────
print("\n── BORROWER DEMOGRAPHICS ──")
print(f"Avg Age:           {df_clean['age'].mean():.1f} yrs")
print(f"Avg Annual Income: ${df_clean['income_annual'].mean():,.0f}")
print(f"Avg Credit Score:  {df_clean['credit_score'].mean():.0f}")
print(f"\nIncome Tier Breakdown:")
print(df_clean["income_tier"].value_counts().sort_index())
print(f"\nCredit Tier Breakdown:")
print(df_clean["credit_tier"].value_counts().sort_index())
print(f"\nEmployment Status:")
print(df_clean["employment_status"].value_counts())
print(f"\nHome Ownership:")
print(df_clean["home_ownership"].value_counts())

# ── Loan Profile ─────────────────────────────────────────────────
print("\n── LOAN PROFILE ──")
print(f"Avg Loan Amount:   ${df_clean['loan_amount'].mean():,.0f}")
print(f"Avg Interest Rate: {df_clean['interest_rate'].mean():.2f}%")
print(f"Avg Loan Term:     {df_clean['loan_term_months'].mean():.0f} months")
print(f"\nLoan Size Breakdown:")
print(df_clean["loan_size"].value_counts().sort_index())
print(f"\nLoan Purpose Breakdown:")
print(df_clean["loan_purpose"].value_counts())
print(f"\nLoan Grade Breakdown:")
print(df_clean["loan_grade"].value_counts().sort_index())

# ── Default Rate by Key Segments ─────────────────────────────────
print("\n── DEFAULT RATE BY KEY SEGMENTS ──")

print(f"\nDefault Rate by Credit Tier:")
print(
    df_clean.groupby("credit_tier", observed=True)["defaulted"]
    .mean().mul(100).round(2).to_string()
)

print(f"\nDefault Rate by Loan Grade:")
print(
    df_clean.groupby("loan_grade")["defaulted"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False).to_string()
)

print(f"\nDefault Rate by Employment Status:")
print(
    df_clean.groupby("employment_status")["defaulted"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False).to_string()
)

print(f"\nDefault Rate by Income Tier:")
print(
    df_clean.groupby("income_tier", observed=True)["defaulted"]
    .mean().mul(100).round(2).to_string()
)

print(f"\nDefault Rate by Home Ownership:")
print(
    df_clean.groupby("home_ownership")["defaulted"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False).to_string()
)

print(f"\nDefault Rate by Loan Purpose:")
print(
    df_clean.groupby("loan_purpose")["defaulted"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False).to_string()
)

# ── Risk Metrics ─────────────────────────────────────────────────
print("\n── RISK METRICS ──")
print(f"Avg Debt-to-Income:      {df_clean['debt_to_income'].mean():.4f}")
print(f"Avg Payment-to-Income:   {df_clean['payment_to_income'].mean():.4f}")
print(f"Avg Total Debt Ratio:    {df_clean['total_debt_ratio'].mean():.4f}")
print(f"Avg Late Payments (2yr): {df_clean['late_payments_2yr'].mean():.2f}")
print(f"Avg Hard Inquiries:      {df_clean['num_hard_inquiries'].mean():.2f}")

print(f"\nAvg Debt-to-Income by Default Status:")
print(df_clean.groupby("defaulted")["debt_to_income"].mean().round(4))

print(f"\nAvg Credit Score by Default Status:")
print(df_clean.groupby("defaulted")["credit_score"].mean().round(2))

print(f"\nAvg Late Payments by Default Status:")
print(df_clean.groupby("defaulted")["late_payments_2yr"].mean().round(2))

print("\n✓ Phase 1 complete. Clean data ready for ML pipeline.")