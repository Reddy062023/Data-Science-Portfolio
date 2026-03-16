# Tests — Data Quality & Validation Framework

## Overview
Production-grade automated testing and validation framework covering all 3 portfolio projects.
Runs 57 automated tests across 6 test suites to ensure data integrity, statistical sanity,
ML model quality, and drift detection.
Generates both an **HTML visual report** and a **CSV results file** on every run.

---

## Project Structure
```
Tests/
├── phase4_data_testing.py    # Main test script
├── test_report.html          # Visual HTML report (auto-generated)
├── test_results.csv          # CSV results with history (auto-generated)
└── README.md
```

---

## Test Suites

### Suite 1 — Schema Validation (23 tests)
- Validates required columns exist in all 3 datasets
- Covers Sales (8 columns), Finance (7 columns), Healthcare (8 columns)

### Suite 2 — Raw Data Quality (8 tests)
- Tests raw data BEFORE Phase 1 cleaning
- Shows what issues existed and were fixed
- Null rate thresholds, duplicate detection, range checks

### Suite 3 — Clean Data Quality (11 tests)
- Tests clean data AFTER Phase 1 cleaning
- Validates duplicates removed, nulls filled
- Confirms feature engineering columns created correctly

### Suite 4 — Statistical Sanity (7 tests)
- Class balance checks
- Coefficient of variation checks
- Correlation direction validation

### Suite 5 — ML Model Sanity (5 tests)
- AUC > 0.65 threshold
- 5-fold cross-validation AUC > 0.60
- Overfitting gap < 0.10
- Both classes predicted
- No train/test data leakage

### Suite 6 — Data Drift Detection (3 tests)
- Normalised mean shift between baseline and new batch
- Covers income, credit score, loan amount

---

## Latest Test Results

| Metric | Result |
|--------|--------|
| Total Tests | 57 |
| ✅ Passed | 55 |
| ❌ Failed | 2 |
| ⚠️ Warnings | 0 |

### Per Suite Breakdown

| Suite | Total | ✅ Passed | ❌ Failed | ⚠️ Warnings | Status |
|-------|-------|-----------|-----------|-------------|--------|
| Suite 1 - Schema | 23 | 23 | 0 | 0 | ✅ PASS |
| Suite 2 - Raw Quality | 8 | 6 | 2 | 0 | ❌ FAIL (expected) |
| Suite 3 - Clean Quality | 11 | 11 | 0 | 0 | ✅ PASS |
| Suite 4 - Statistical | 7 | 7 | 0 | 0 | ✅ PASS |
| Suite 5 - ML Model | 5 | 5 | 0 | 0 | ✅ PASS |
| Suite 6 - Drift Detection | 3 | 3 | 0 | 0 | ✅ PASS |

### Failed Tests Explanation
| Test | Detail | Why Expected |
|------|--------|--------------|
| `sales: no duplicate order_ids` | 20 dupes in raw data | Fixed in Phase 1 — clean data passes ✅ |
| `sales: quantity all positive` | 5 invalid rows in raw data | Fixed in Phase 1 — clean data passes ✅ |

> **Note:** Suite 2 intentionally tests RAW data to document what issues existed before cleaning.
> Suite 3 confirms all issues are resolved in the clean data.

---

## Output Files

| File | Description |
|------|-------------|
| `test_report.html` | Visual dashboard with colored cards — open in browser |
| `test_results.csv` | Timestamped results — appends on every run to build history |

---

## Datasets Tested

| Dataset | Location | Raw Shape | Clean Shape |
|---------|----------|-----------|-------------|
| Sales | `Sales-EDA/` | 520 × 15 | 472 × 19 |
| Healthcare | `Healthcare-Visualization/` | 800 × 22 | 770 × 26 |
| Finance | `Finance-ML/` | 1000 × 20 | 960 × 29 |

---

## Setup & Usage

### 1. Activate your environment
```bash
conda activate myenv
```

### 2. Install dependencies
```bash
pip install numpy pandas scikit-learn
```

### 3. Run tests
```bash
cd Tests
python phase4_data_testing.py
```

### 4. View results
- Open `test_report.html` in browser for visual dashboard
- Open `test_results.csv` in Excel for historical results

---

## Requirements
| Package | Version |
|---------|---------|
| Python | 3.13+ |
| pandas | latest |
| numpy | latest |
| scikit-learn | latest |

---

## Author
**Japendra**
Data Analysis Portfolio — Data Testing & Validation Framework