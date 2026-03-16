"""
Phase 1: Exploratory Data Analysis — Healthcare Data
Approach: Senior Lead / Data Scientist perspective
Dataset: healthcare_data.csv (800 rows, 22 columns)
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
df = pd.read_csv(BASE_DIR / "healthcare_data.csv")
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

profile = profile_dataframe(df, "Healthcare")

# ─────────────────────────────────────────────────────────────────
# 3. DETECT & HANDLE DATA QUALITY ISSUES
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3 — DATA QUALITY ISSUES")
print("=" * 60)

# Duplicate check
dupes = df.duplicated(subset="patient_id").sum()
print(f"Duplicate patient_ids: {dupes}")

# Null summary
null_summary = df.isnull().sum()
null_summary = null_summary[null_summary > 0]
print(f"\nColumns with nulls:\n{null_summary}")

# Out-of-range checks
neg_age = (df["age"] <= 0).sum()
neg_bmi = (df["bmi"] <= 0).sum()
neg_bp  = (df["blood_pressure_systolic"] <= 0).sum()
print(f"\nInvalid age rows:      {neg_age}")
print(f"Invalid BMI rows:      {neg_bmi}")
print(f"Invalid systolic BP:   {neg_bp}")

# Key categorical distributions
print(f"\nDiagnosis value counts:\n{df['diagnosis'].value_counts(dropna=False)}")
print(f"\nGender value counts:\n{df['gender'].value_counts(dropna=False)}")
print(f"\nInsurance type value counts:\n{df['insurance_type'].value_counts(dropna=False)}")
print(f"\nSmoker value counts:\n{df['smoker'].value_counts(dropna=False)}")
print(f"\nDiabetic value counts:\n{df['diabetic'].value_counts(dropna=False)}")

# ─── Clean ───────────────────────────────────────────────────────
df_clean = df.copy()

# Remove duplicates
df_clean = df_clean.drop_duplicates(subset="patient_id", keep="first")

# Remove invalid rows
df_clean = df_clean[df_clean["age"] > 0]
df_clean = df_clean[df_clean["bmi"] > 0]
df_clean = df_clean[df_clean["blood_pressure_systolic"] > 0]

# Fill numeric nulls with median
for col in ["bmi", "glucose_level", "cholesterol_total",
            "blood_pressure_systolic", "blood_pressure_diastolic",
            "exercise_hrs_week", "medication_count"]:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())

# Fill categorical nulls
df_clean["smoker"]         = df_clean["smoker"].fillna(0)
df_clean["diabetic"]       = df_clean["diabetic"].fillna(0)
df_clean["readmitted_30d"] = df_clean["readmitted_30d"].fillna(0)
df_clean["gender"]         = df_clean["gender"].fillna("Unknown")
df_clean["insurance_type"] = df_clean["insurance_type"].fillna("Unknown")
df_clean["diagnosis"]      = df_clean["diagnosis"].fillna("Unknown")

# ─── Feature engineering ─────────────────────────────────────────
df_clean["age_group"] = pd.cut(
    df_clean["age"],
    bins=[0, 18, 35, 50, 65, 120],
    labels=["<18", "18-35", "35-50", "50-65", "65+"]
)

df_clean["bmi_category"] = pd.cut(
    df_clean["bmi"],
    bins=[0, 18.5, 25, 30, 100],
    labels=["Underweight", "Normal", "Overweight", "Obese"]
)

df_clean["bp_category"] = pd.cut(
    df_clean["blood_pressure_systolic"],
    bins=[0, 120, 130, 140, 300],
    labels=["Normal", "Elevated", "High Stage 1", "High Stage 2"]
)

df_clean["high_risk"] = (
    (df_clean["smoker"] == 1) |
    (df_clean["diabetic"] == 1) |
    (df_clean["bmi"] >= 30) |
    (df_clean["blood_pressure_systolic"] >= 140)
).astype(int)

print(f"\nClean shape: {df_clean.shape}")
print(f"Remaining nulls:\n{df_clean.isnull().sum()[df_clean.isnull().sum() > 0]}")

# ─────────────────────────────────────────────────────────────────
# EXPORT CLEAN DATA — same folder as script
# ─────────────────────────────────────────────────────────────────
output_path = BASE_DIR / "healthcare_data_clean.csv"
df_clean.to_csv(output_path, index=False)
print(f"\n✓ Clean data saved → {output_path}  ({df_clean.shape[0]} rows × {df_clean.shape[1]} cols)")

# ─────────────────────────────────────────────────────────────────
# 4. BUSINESS INSIGHTS
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4 — BUSINESS INSIGHTS")
print("=" * 60)

# ── Patient Demographics ─────────────────────────────────────────
print("\n── PATIENT DEMOGRAPHICS ──")
print(f"Total Patients:     {len(df_clean):,}")
print(f"Avg Age:            {df_clean['age'].mean():.1f} yrs")
print(f"Age Range:          {df_clean['age'].min():.0f} – {df_clean['age'].max():.0f} yrs")
print(f"\nGender Breakdown:")
print(df_clean["gender"].value_counts())
print(f"\nAge Group Breakdown:")
print(df_clean["age_group"].value_counts().sort_index())
print(f"\nInsurance Type Breakdown:")
print(df_clean["insurance_type"].value_counts())

# ── Clinical Metrics ─────────────────────────────────────────────
print("\n── CLINICAL METRICS ──")
clinical_cols = ["bmi", "blood_pressure_systolic", "blood_pressure_diastolic",
                 "cholesterol_total", "glucose_level"]
print(df_clean[clinical_cols].describe().T[["mean", "50%", "std", "min", "max"]]
      .rename(columns={"50%": "median"}))

print(f"\nBMI Category Breakdown:")
print(df_clean["bmi_category"].value_counts())
print(f"\nBP Category Breakdown:")
print(df_clean["bp_category"].value_counts())

# ── Diagnosis Breakdown ──────────────────────────────────────────
print("\n── DIAGNOSIS BREAKDOWN ──")
diag_summary = df_clean.groupby("diagnosis").agg(
    patients   = ("patient_id", "count"),
    avg_age    = ("age", "mean"),
    avg_bmi    = ("bmi", "mean"),
    avg_bp     = ("blood_pressure_systolic", "mean"),
    avg_days   = ("hospital_days", "mean")
).round(2)
diag_summary["share_%"] = (diag_summary["patients"] / len(df_clean) * 100).round(2)
print(diag_summary.sort_values("patients", ascending=False))

# ── Readmission Analysis ─────────────────────────────────────────
print("\n── READMISSION ANALYSIS ──")
overall_readmit = df_clean["readmitted_30d"].mean() * 100
print(f"Overall 30-day Readmission Rate: {overall_readmit:.1f}%")

print(f"\nReadmission Rate by Diagnosis:")
print(
    df_clean.groupby("diagnosis")["readmitted_30d"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False).to_string()
)

print(f"\nReadmission Rate by Insurance Type:")
print(
    df_clean.groupby("insurance_type")["readmitted_30d"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False).to_string()
)

print(f"\nReadmission Rate by Age Group:")
print(
    df_clean.groupby("age_group", observed=True)["readmitted_30d"]
    .mean().mul(100).round(2).to_string()
)

# ── Smoking & Diabetes Risk ──────────────────────────────────────
print("\n── SMOKING & DIABETES RISK ──")
smoker_pct    = df_clean["smoker"].mean() * 100
diabetic_pct  = df_clean["diabetic"].mean() * 100
high_risk_pct = df_clean["high_risk"].mean() * 100

print(f"Smoker Rate:          {smoker_pct:.1f}%")
print(f"Diabetic Rate:        {diabetic_pct:.1f}%")
print(f"High Risk Patients:   {high_risk_pct:.1f}%")

print(f"\nCritical Diagnosis Rate — Smokers vs Non-Smokers:")
for val, label in [(1, "Smoker"), (0, "Non-Smoker")]:
    rate = (df_clean[df_clean["smoker"] == val]["diagnosis"] == "Critical").mean() * 100
    print(f"  {label:<12}: {rate:.1f}%")

print(f"\nCritical Diagnosis Rate — Diabetic vs Non-Diabetic:")
for val, label in [(1, "Diabetic"), (0, "Non-Diabetic")]:
    rate = (df_clean[df_clean["diabetic"] == val]["diagnosis"] == "Critical").mean() * 100
    print(f"  {label:<14}: {rate:.1f}%")

print(f"\nAvg Cholesterol by Smoker Status:")
print(df_clean.groupby("smoker")["cholesterol_total"].mean().round(2))

# ── Hospital Stay Analysis ───────────────────────────────────────
print("\n── HOSPITAL STAY ANALYSIS ──")
print(f"Avg Hospital Days (All):       {df_clean['hospital_days'].mean():.1f}")
print(f"Median Hospital Days:          {df_clean['hospital_days'].median():.1f}")
print(f"Max Hospital Days:             {df_clean['hospital_days'].max():.0f}")

print(f"\nAvg Hospital Days by Diagnosis:")
print(
    df_clean.groupby("diagnosis")["hospital_days"]
    .mean().round(2)
    .sort_values(ascending=False).to_string()
)

print(f"\nAvg Hospital Days by Age Group:")
print(
    df_clean.groupby("age_group", observed=True)["hospital_days"]
    .mean().round(2).to_string()
)

print(f"\nAvg Medication Count by Diagnosis:")
print(
    df_clean.groupby("diagnosis")["medication_count"]
    .mean().round(2)
    .sort_values(ascending=False).to_string()
)

print("\n✓ Phase 1 complete. Clean data ready for visualization.")