"""
Phase 4: Data Testing & Validation — All 3 Datasets
Approach: Production-grade data quality framework
Covers: Schema tests, statistical tests, model tests, drift detection
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

# ─────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent

# ─────────────────────────────────────────────────────────────────
# TEST RUNNER — lightweight framework (no pytest dependency)
# ─────────────────────────────────────────────────────────────────
class TestRunner:
    def __init__(self):
        self.passed   = []
        self.failed   = []
        self.warnings = []

    def check(self, name, condition, detail="", severity="FAIL"):
        if condition:
            self.passed.append(name)
            print(f"  ✓ PASS  {name}")
        else:
            if severity == "WARN":
                self.warnings.append(f"{name}: {detail}")
                print(f"  ⚠ WARN  {name}  → {detail}")
            else:
                self.failed.append(f"{name}: {detail}")
                print(f"  ✗ FAIL  {name}  → {detail}")

    def summary(self):
        total = len(self.passed) + len(self.failed) + len(self.warnings)
        print("\n" + "═" * 60)
        print(f"RESULTS: {len(self.passed)} passed  |  {len(self.failed)} failed  |  {len(self.warnings)} warnings  |  {total} total")
        if self.failed:
            print("\nFailed tests:")
            for f in self.failed:
                print(f"  ✗ {f}")
        if self.warnings:
            print("\nWarnings:")
            for w in self.warnings:
                print(f"  ⚠ {w}")
        print("═" * 60)
        return len(self.failed) == 0

t = TestRunner()

# ─────────────────────────────────────────────────────────────────
# LOAD DATASETS
# ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("LOADING DATASETS")
print("=" * 60)

sales   = pd.read_csv(ROOT_DIR / "Sales-EDA"                / "sales_data.csv")
health  = pd.read_csv(ROOT_DIR / "Healthcare-Visualization"  / "healthcare_data.csv")
finance = pd.read_csv(ROOT_DIR / "Finance-ML"               / "finance_data.csv")

print(f"Sales:      {sales.shape}")
print(f"Healthcare: {health.shape}")
print(f"Finance:    {finance.shape}")

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 1 — SCHEMA VALIDATION
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 1 — SCHEMA VALIDATION")
print("=" * 60)

SALES_SCHEMA = {
    "order_id":   "object",
    "customer_id":"object",
    "product":    "object",
    "quantity":   "int64",
    "unit_price": "float64",
    "returned":   "object",
    "order_date": "object",
    "region":     "object"
}

for col, expected_dtype in SALES_SCHEMA.items():
    t.check(f"sales.{col} exists", col in sales.columns,
            detail=f"Column '{col}' missing")
    if col in sales.columns:
        t.check(f"sales.{col} dtype={expected_dtype}",
                str(sales[col].dtype) == expected_dtype or
                expected_dtype in str(sales[col].dtype),
                detail=f"Expected {expected_dtype}, got {sales[col].dtype}",
                severity="WARN")

FINANCE_REQUIRED = ["customer_id","age","income_annual","credit_score",
                     "loan_amount","loan_term_months","defaulted"]
for col in FINANCE_REQUIRED:
    t.check(f"finance.{col} exists", col in finance.columns)

HEALTH_REQUIRED = ["patient_id","age","gender","bmi","blood_pressure_systolic",
                    "diagnosis","hospital_days","readmitted_30d"]
for col in HEALTH_REQUIRED:
    t.check(f"healthcare.{col} exists", col in health.columns)

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 2 — DATA QUALITY
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 2 — DATA QUALITY")
print("=" * 60)

# Null thresholds
t.check("sales: null rate < 15%",
        (sales.isnull().sum() / len(sales)).max() < 0.15,
        detail=f"Max null rate: {(sales.isnull().sum()/len(sales)).max():.1%}")

t.check("healthcare: null rate < 10%",
        (health.isnull().sum() / len(health)).max() < 0.10,
        detail=f"Max null rate: {(health.isnull().sum()/len(health)).max():.1%}",
        severity="WARN")

t.check("finance: null rate < 15%",
        (finance.isnull().sum() / len(finance)).max() < 0.15,
        detail=f"Max null rate: {(finance.isnull().sum()/len(finance)).max():.1%}")

# Duplicate checks
t.check("sales: no duplicate order_ids",
        sales.duplicated(subset="order_id").sum() == 0,
        detail=f"{sales.duplicated(subset='order_id').sum()} dupes found")

t.check("healthcare: no duplicate patient_ids",
        health.duplicated(subset="patient_id").sum() == 0,
        detail=f"{health.duplicated(subset='patient_id').sum()} dupes found")

t.check("finance: no duplicate customer_ids",
        finance.duplicated(subset="customer_id").sum() == 0,
        detail=f"{finance.duplicated(subset='customer_id').sum()} dupes found")

# Range / domain constraints
t.check("sales: quantity all positive",
        (sales["quantity"].dropna() > 0).all(),
        detail=f"{(sales['quantity'].dropna() <= 0).sum()} invalid rows")

t.check("finance: credit_score in [300, 850]",
        finance["credit_score"].dropna().between(300, 850).all(),
        detail=f"{(~finance['credit_score'].dropna().between(300,850)).sum()} out-of-range")

t.check("finance: loan_term_months valid",
        finance["loan_term_months"].isin([12,24,36,48,60,72]).all(),
        detail=f"Unexpected values: {finance['loan_term_months'].unique().tolist()}")

t.check("finance: defaulted is binary",
        finance["defaulted"].isin([0,1]).all(),
        detail="Non-binary values found")

t.check("healthcare: age in [0, 120]",
        health["age"].between(0, 120).all(),
        detail=f"{(~health['age'].between(0,120)).sum()} invalid ages")

t.check("healthcare: bmi in [10, 70]",
        health["bmi"].dropna().between(10, 70).all(),
        detail=f"{(~health['bmi'].dropna().between(10,70)).sum()} outlier BMIs",
        severity="WARN")

# Referential integrity
valid_diagnoses    = {"Healthy","At Risk","Critical"}
actual_diagnoses   = set(health["diagnosis"].dropna().unique())
t.check("healthcare: diagnosis values valid",
        actual_diagnoses.issubset(valid_diagnoses),
        detail=f"Unknown values: {actual_diagnoses - valid_diagnoses}")

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 3 — STATISTICAL SANITY CHECKS
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 3 — STATISTICAL SANITY")
print("=" * 60)

# Class balance
default_rate = finance["defaulted"].mean()
t.check("finance: default rate in [5%, 60%]",
        0.05 <= default_rate <= 0.60,
        detail=f"Default rate: {default_rate:.3f}")

healthy_rate = (health["diagnosis"] == "Healthy").mean()
t.check("healthcare: healthy rate > 5%",
        healthy_rate > 0.05,
        detail=f"Healthy rate: {healthy_rate:.3f}")

# Distribution checks
for col in ["income_annual","credit_score","loan_amount"]:
    cv_coef = finance[col].dropna().std() / finance[col].dropna().mean()
    t.check(f"finance: {col} has meaningful variance (CV > 0.1)",
            cv_coef > 0.1,
            detail=f"CV = {cv_coef:.3f}")

# Correlation sanity
corr = finance[["credit_score","defaulted"]].dropna().corr().iloc[0,1]
t.check("finance: credit_score negatively correlated with default",
        corr < -0.05,
        detail=f"Correlation: {corr:.4f}")

income_corr = finance[["income_annual","defaulted"]].dropna().corr().iloc[0,1]
t.check("finance: income negatively correlated with default",
        income_corr < 0,
        detail=f"Correlation: {income_corr:.4f}")

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 4 — ML MODEL TESTS
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 4 — ML MODEL SANITY")
print("=" * 60)

fin_clean = finance.copy()
fin_clean["credit_score"]  = fin_clean["credit_score"].fillna(fin_clean["credit_score"].median())
fin_clean["income_annual"] = fin_clean["income_annual"].fillna(fin_clean["income_annual"].median())
for col in ["employment_status","loan_purpose","home_ownership","loan_grade","gender"]:
    fin_clean[col] = LabelEncoder().fit_transform(fin_clean[col].astype(str))

features = ["age","income_annual","credit_score","loan_amount","loan_term_months",
            "employment_years","late_payments_2yr","interest_rate",
            "employment_status","loan_purpose","loan_grade"]

X = fin_clean[features]
y = fin_clean["defaulted"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

model = Pipeline([
    ("imp", SimpleImputer(strategy="median")),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42,
                                   class_weight="balanced"))
])
model.fit(X_train, y_train)

auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
t.check("model: AUC > 0.65 (beats random significantly)",
        auc > 0.65,
        detail=f"AUC = {auc:.4f}")

cv_auc = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
t.check("model: CV AUC > 0.60 (generalises)",
        cv_auc.mean() > 0.60,
        detail=f"CV AUC = {cv_auc.mean():.4f} ± {cv_auc.std():.4f}")

overfit_gap = auc - cv_auc.mean()
t.check("model: overfit gap < 0.10",
        abs(overfit_gap) < 0.10,
        detail=f"Gap = {overfit_gap:.4f}",
        severity="WARN")

preds = model.predict(X_test)
t.check("model: predicts both classes",
        len(set(preds)) == 2,
        detail=f"Only predicts: {set(preds)}")

overlap = set(X_train.index) & set(X_test.index)
t.check("model: no train/test index overlap",
        len(overlap) == 0,
        detail=f"{len(overlap)} overlapping indices")

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 5 — DATA DRIFT DETECTION
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 5 — DATA DRIFT DETECTION")
print("=" * 60)

baseline  = finance.iloc[:500]
new_batch = finance.iloc[500:]

def check_distribution_drift(baseline, new_batch, col, threshold=0.15):
    base_vals         = baseline[col].dropna()
    new_vals          = new_batch[col].dropna()
    mean_shift        = abs(new_vals.mean() - base_vals.mean())
    std_base          = base_vals.std()
    normalised_shift  = mean_shift / (std_base + 1e-9)
    return normalised_shift < threshold, normalised_shift

for col in ["income_annual","credit_score","loan_amount"]:
    no_drift, shift = check_distribution_drift(baseline, new_batch, col)
    t.check(f"drift: {col} stable between batches",
            no_drift,
            detail=f"Normalised shift: {shift:.4f}",
            severity="WARN")

# ─────────────────────────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────────────────────────
print()
all_passed = t.summary()
if all_passed:
    print("\n✓ All tests passed — data pipeline is production-ready.")
else:
    print("\n✗ Some tests failed — review before deploying to production.")