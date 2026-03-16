"""
Phase 4: Data Testing & Validation — All 3 Datasets
Approach: Production-grade data quality framework
Covers: Schema tests, statistical tests, model tests, drift detection
Tests both RAW and CLEAN data to show Phase 1 cleaning effectiveness
"""

import numpy as np
import pandas as pd
import warnings
import datetime
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
# TEST RUNNER
# ─────────────────────────────────────────────────────────────────
class TestRunner:
    def __init__(self, name=""):
        self.name     = name
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
        print(f"[{self.name}] RESULTS: {len(self.passed)} passed  |  "
              f"{len(self.failed)} failed  |  {len(self.warnings)} warnings  |  {total} total")
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

# ─────────────────────────────────────────────────────────────────
# LOAD DATASETS — RAW
# ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("LOADING RAW DATASETS")
print("=" * 60)

sales_raw   = pd.read_csv(ROOT_DIR / "Sales-EDA"               / "sales_data.csv")
health_raw  = pd.read_csv(ROOT_DIR / "Healthcare-Visualization" / "healthcare_data.csv")
finance_raw = pd.read_csv(ROOT_DIR / "Finance-ML"              / "finance_data.csv")

print(f"Sales raw:      {sales_raw.shape}")
print(f"Healthcare raw: {health_raw.shape}")
print(f"Finance raw:    {finance_raw.shape}")

# ─────────────────────────────────────────────────────────────────
# LOAD DATASETS — CLEAN
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("LOADING CLEAN DATASETS")
print("=" * 60)

sales_clean   = pd.read_csv(ROOT_DIR / "Sales-EDA"               / "sales_data_clean.csv")
health_clean  = pd.read_csv(ROOT_DIR / "Healthcare-Visualization" / "healthcare_data_clean.csv")
finance_clean = pd.read_csv(ROOT_DIR / "Finance-ML"              / "finance_data_clean.csv")

print(f"Sales clean:      {sales_clean.shape}")
print(f"Healthcare clean: {health_clean.shape}")
print(f"Finance clean:    {finance_clean.shape}")

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 1 — SCHEMA VALIDATION
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 1 — SCHEMA VALIDATION (Raw Data)")
print("=" * 60)

t1 = TestRunner("Suite 1 - Schema")

SALES_SCHEMA = {
    "order_id":    "object",
    "customer_id": "object",
    "product":     "object",
    "quantity":    "int64",
    "unit_price":  "float64",
    "returned":    "object",
    "order_date":  "object",
    "region":      "object"
}

for col, expected_dtype in SALES_SCHEMA.items():
    t1.check(f"sales.{col} exists", col in sales_raw.columns,
             detail=f"Column '{col}' missing")

FINANCE_REQUIRED = ["customer_id","age","income_annual","credit_score",
                     "loan_amount","loan_term_months","defaulted"]
for col in FINANCE_REQUIRED:
    t1.check(f"finance.{col} exists", col in finance_raw.columns)

HEALTH_REQUIRED = ["patient_id","age","gender","bmi","blood_pressure_systolic",
                    "diagnosis","hospital_days","readmitted_30d"]
for col in HEALTH_REQUIRED:
    t1.check(f"healthcare.{col} exists", col in health_raw.columns)

t1.summary()

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 2 — RAW DATA QUALITY (Before Cleaning)
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 2 — RAW DATA QUALITY (Before Cleaning)")
print("=" * 60)

t2_raw = TestRunner("Suite 2 - Raw Quality")

t2_raw.check("sales: null rate < 15%",
             (sales_raw.isnull().sum() / len(sales_raw)).max() < 0.15,
             detail=f"Max null rate: {(sales_raw.isnull().sum()/len(sales_raw)).max():.1%}")

t2_raw.check("sales: no duplicate order_ids",
             sales_raw.duplicated(subset="order_id").sum() == 0,
             detail=f"{sales_raw.duplicated(subset='order_id').sum()} dupes found")

t2_raw.check("sales: quantity all positive",
             (sales_raw["quantity"].dropna() > 0).all(),
             detail=f"{(sales_raw['quantity'].dropna() <= 0).sum()} invalid rows")

t2_raw.check("healthcare: no duplicate patient_ids",
             health_raw.duplicated(subset="patient_id").sum() == 0,
             detail=f"{health_raw.duplicated(subset='patient_id').sum()} dupes found")

t2_raw.check("finance: no duplicate customer_ids",
             finance_raw.duplicated(subset="customer_id").sum() == 0,
             detail=f"{finance_raw.duplicated(subset='customer_id').sum()} dupes found")

t2_raw.check("finance: credit_score in [300, 850]",
             finance_raw["credit_score"].dropna().between(300, 850).all(),
             detail=f"{(~finance_raw['credit_score'].dropna().between(300,850)).sum()} out-of-range")

t2_raw.check("finance: defaulted is binary",
             finance_raw["defaulted"].isin([0,1]).all(),
             detail="Non-binary values found")

t2_raw.check("healthcare: age in [0, 120]",
             health_raw["age"].between(0, 120).all(),
             detail=f"{(~health_raw['age'].between(0,120)).sum()} invalid ages")

t2_raw.summary()

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 3 — CLEAN DATA QUALITY (After Phase 1)
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 3 — CLEAN DATA QUALITY (After Phase 1 Cleaning)")
print("=" * 60)

t3_clean = TestRunner("Suite 3 - Clean Quality")

t3_clean.check("sales clean: null rate < 10%",
               (sales_clean.isnull().sum() / len(sales_clean)).max() < 0.10,
               detail=f"Max null rate: {(sales_clean.isnull().sum()/len(sales_clean)).max():.1%}")

t3_clean.check("sales clean: no duplicate order_ids",
               sales_clean.duplicated(subset="order_id").sum() == 0,
               detail=f"{sales_clean.duplicated(subset='order_id').sum()} dupes found")

t3_clean.check("sales clean: quantity all positive",
               (sales_clean["quantity"].dropna() > 0).all(),
               detail=f"{(sales_clean['quantity'].dropna() <= 0).sum()} invalid rows")

t3_clean.check("healthcare clean: no duplicate patient_ids",
               health_clean.duplicated(subset="patient_id").sum() == 0,
               detail=f"{health_clean.duplicated(subset='patient_id').sum()} dupes found")

t3_clean.check("finance clean: no duplicate customer_ids",
               finance_clean.duplicated(subset="customer_id").sum() == 0,
               detail=f"{finance_clean.duplicated(subset='customer_id').sum()} dupes found")

t3_clean.check("finance clean: credit_score in [300, 850]",
               finance_clean["credit_score"].dropna().between(300, 850).all(),
               detail=f"{(~finance_clean['credit_score'].dropna().between(300,850)).sum()} out-of-range")

t3_clean.check("finance clean: no nulls in key columns",
               finance_clean[["credit_score","income_annual","loan_amount"]].isnull().sum().sum() == 0,
               detail="Nulls found in key columns")

t3_clean.check("healthcare clean: no nulls in key columns",
               health_clean[["bmi","glucose_level","cholesterol_total"]].isnull().sum().sum() == 0,
               detail="Nulls found in key columns")

t3_clean.check("sales clean: revenue column exists",
               "revenue" in sales_clean.columns,
               detail="revenue column missing — feature engineering failed")

t3_clean.check("healthcare clean: age_group column exists",
               "age_group" in health_clean.columns,
               detail="age_group column missing — feature engineering failed")

t3_clean.check("finance clean: debt_to_income column exists",
               "debt_to_income" in finance_clean.columns,
               detail="debt_to_income column missing — feature engineering failed")

t3_clean.summary()

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 4 — STATISTICAL SANITY
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 4 — STATISTICAL SANITY")
print("=" * 60)

t4 = TestRunner("Suite 4 - Statistical")

default_rate = finance_clean["defaulted"].mean()
t4.check("finance: default rate in [5%, 60%]",
         0.05 <= default_rate <= 0.60,
         detail=f"Default rate: {default_rate:.3f}")

healthy_rate = (health_clean["diagnosis"] == "Healthy").mean()
t4.check("healthcare: healthy rate > 5%",
         healthy_rate > 0.05,
         detail=f"Healthy rate: {healthy_rate:.3f}")

for col in ["income_annual","credit_score","loan_amount"]:
    cv_coef = finance_clean[col].dropna().std() / finance_clean[col].dropna().mean()
    t4.check(f"finance: {col} has meaningful variance (CV > 0.1)",
             cv_coef > 0.1,
             detail=f"CV = {cv_coef:.3f}")

corr = finance_clean[["credit_score","defaulted"]].dropna().corr().iloc[0,1]
t4.check("finance: credit_score negatively correlated with default",
         corr < -0.05,
         detail=f"Correlation: {corr:.4f}")

income_corr = finance_clean[["income_annual","defaulted"]].dropna().corr().iloc[0,1]
t4.check("finance: income negatively correlated with default",
         income_corr < 0,
         detail=f"Correlation: {income_corr:.4f}")

t4.summary()

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 5 — ML MODEL SANITY
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 5 — ML MODEL SANITY")
print("=" * 60)

t5 = TestRunner("Suite 5 - ML Model")

fin_clean = finance_clean.copy()
fin_clean["defaulted"] = fin_clean["defaulted"].astype(int)
for col in ["employment_status","loan_purpose","home_ownership","loan_grade","gender"]:
    if col in fin_clean.columns:
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
t5.check("model: AUC > 0.65 (beats random significantly)",
         auc > 0.65, detail=f"AUC = {auc:.4f}")

cv_auc = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
t5.check("model: CV AUC > 0.60 (generalises)",
         cv_auc.mean() > 0.60,
         detail=f"CV AUC = {cv_auc.mean():.4f} ± {cv_auc.std():.4f}")

overfit_gap = auc - cv_auc.mean()
t5.check("model: overfit gap < 0.10",
         abs(overfit_gap) < 0.10,
         detail=f"Gap = {overfit_gap:.4f}", severity="WARN")

preds = model.predict(X_test)
t5.check("model: predicts both classes",
         len(set(preds)) == 2,
         detail=f"Only predicts: {set(preds)}")

overlap = set(X_train.index) & set(X_test.index)
t5.check("model: no train/test index overlap",
         len(overlap) == 0,
         detail=f"{len(overlap)} overlapping indices")

t5.summary()

# ─────────────────────────────────────────────────────────────────
# TEST SUITE 6 — DATA DRIFT DETECTION
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TEST SUITE 6 — DATA DRIFT DETECTION")
print("=" * 60)

t6 = TestRunner("Suite 6 - Drift Detection")

baseline  = finance_raw.iloc[:500]
new_batch = finance_raw.iloc[500:]

def check_distribution_drift(baseline, new_batch, col, threshold=0.15):
    base_vals        = baseline[col].dropna()
    new_vals         = new_batch[col].dropna()
    mean_shift       = abs(new_vals.mean() - base_vals.mean())
    std_base         = base_vals.std()
    normalised_shift = mean_shift / (std_base + 1e-9)
    return normalised_shift < threshold, normalised_shift

for col in ["income_annual","credit_score","loan_amount"]:
    no_drift, shift = check_distribution_drift(baseline, new_batch, col)
    t6.check(f"drift: {col} stable between batches",
             no_drift,
             detail=f"Normalised shift: {shift:.4f}",
             severity="WARN")

t6.summary()

# ─────────────────────────────────────────────────────────────────
# OVERALL SUMMARY
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("OVERALL PORTFOLIO TEST SUMMARY")
print("=" * 60)

all_runners    = [t1, t2_raw, t3_clean, t4, t5, t6]
total_passed   = sum(len(t.passed)   for t in all_runners)
total_failed   = sum(len(t.failed)   for t in all_runners)
total_warnings = sum(len(t.warnings) for t in all_runners)
total_tests    = total_passed + total_failed + total_warnings

print(f"\nTotal Tests:    {total_tests}")
print(f"✅ Passed:      {total_passed}")
print(f"❌ Failed:      {total_failed}")
print(f"⚠️  Warnings:   {total_warnings}")

print("\nPer Suite:")
for runner in all_runners:
    total = len(runner.passed) + len(runner.failed) + len(runner.warnings)
    print(f"  {runner.name:<35} "
          f"✓ {len(runner.passed):>2}  "
          f"✗ {len(runner.failed):>2}  "
          f"⚠ {len(runner.warnings):>2}  "
          f"total {total:>2}")

if total_failed == 0:
    print("\n✓ All critical tests passed — data pipeline is production-ready.")
else:
    print(f"\n✗ {total_failed} tests failed — review before deploying to production.")

# ─────────────────────────────────────────────────────────────────
# SAVE HTML REPORT
# ─────────────────────────────────────────────────────────────────
report_path = BASE_DIR / "test_report.html"

html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Quality Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ padding: 20px 30px; border-radius: 8px; color: white; text-align: center; }}
        .card h3 {{ margin: 0; font-size: 36px; }}
        .card p {{ margin: 5px 0 0; font-size: 14px; }}
        .green {{ background: #2ecc71; }}
        .red {{ background: #e74c3c; }}
        .orange {{ background: #f39c12; }}
        .blue {{ background: #3498db; }}
        table {{ width: 100%; border-collapse: collapse; background: white;
                 border-radius: 8px; overflow: hidden; margin-top: 10px; }}
        th {{ background: #2c3e50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #eee; }}
        .pass {{ color: #2ecc71; font-weight: bold; }}
        .fail {{ color: #e74c3c; font-weight: bold; }}
        .warn {{ color: #f39c12; font-weight: bold; }}
        tr:hover {{ background: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>📊 Data Quality Test Report</h1>
    <p>Portfolio: Japendra | Generated automatically by phase4_data_testing.py</p>

    <div class="summary">
        <div class="card blue"><h3>{total_tests}</h3><p>Total Tests</p></div>
        <div class="card green"><h3>{total_passed}</h3><p>✅ Passed</p></div>
        <div class="card red"><h3>{total_failed}</h3><p>❌ Failed</p></div>
        <div class="card orange"><h3>{total_warnings}</h3><p>⚠️ Warnings</p></div>
    </div>

    <h2>Per Suite Summary</h2>
    <table>
        <tr>
            <th>Suite</th><th>Total</th><th>✅ Passed</th>
            <th>❌ Failed</th><th>⚠️ Warnings</th><th>Status</th>
        </tr>
"""

for runner in all_runners:
    total = len(runner.passed) + len(runner.failed) + len(runner.warnings)
    status = "✅ PASS" if len(runner.failed) == 0 else "❌ FAIL"
    status_class = "pass" if len(runner.failed) == 0 else "fail"
    html += f"""
        <tr>
            <td>{runner.name}</td><td>{total}</td>
            <td class="pass">{len(runner.passed)}</td>
            <td class="fail">{len(runner.failed)}</td>
            <td class="warn">{len(runner.warnings)}</td>
            <td class="{status_class}">{status}</td>
        </tr>"""

html += """
    </table>
    <h2>Detailed Test Results</h2>
    <table>
        <tr>
            <th>Suite</th><th>Test</th><th>Result</th><th>Detail</th>
        </tr>
"""

for runner in all_runners:
    for test in runner.passed:
        html += f"""
        <tr>
            <td>{runner.name}</td><td>{test}</td>
            <td class="pass">✅ PASS</td><td>—</td>
        </tr>"""
    for test in runner.failed:
        name, *detail = test.split(":")
        html += f"""
        <tr>
            <td>{runner.name}</td><td>{name}</td>
            <td class="fail">❌ FAIL</td>
            <td>{':'.join(detail).strip()}</td>
        </tr>"""
    for test in runner.warnings:
        name, *detail = test.split(":")
        html += f"""
        <tr>
            <td>{runner.name}</td><td>{name}</td>
            <td class="warn">⚠️ WARN</td>
            <td>{':'.join(detail).strip()}</td>
        </tr>"""

html += "</table></body></html>"

with open(report_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\n✓ HTML report saved → {report_path.name}")

# ─────────────────────────────────────────────────────────────────
# SAVE CSV REPORT
# ─────────────────────────────────────────────────────────────────
rows = []
for runner in all_runners:
    for test in runner.passed:
        rows.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "suite":     runner.name,
            "test":      test,
            "result":    "PASS",
            "detail":    ""
        })
    for test in runner.failed:
        name, *detail = test.split(":")
        rows.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "suite":     runner.name,
            "test":      name.strip(),
            "result":    "FAIL",
            "detail":    ":".join(detail).strip()
        })
    for test in runner.warnings:
        name, *detail = test.split(":")
        rows.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "suite":     runner.name,
            "test":      name.strip(),
            "result":    "WARN",
            "detail":    ":".join(detail).strip()
        })

csv_path = BASE_DIR / "test_results.csv"

if csv_path.exists():
    existing = pd.read_csv(csv_path)
    new_df   = pd.DataFrame(rows)
    combined = pd.concat([existing, new_df], ignore_index=True)
    combined.to_csv(csv_path, index=False)
    print(f"✓ Results appended → {csv_path.name}  "
          f"(total runs: {combined['timestamp'].nunique()})")
else:
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    print(f"✓ Results saved → {csv_path.name}")

print("\n✓ Phase 4 complete.")