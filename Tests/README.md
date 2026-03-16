# Tests — Data Quality & Validation Framework

## Overview
Production-grade data testing and validation framework covering all 3 portfolio projects.
Runs 59 automated tests across 5 test suites to ensure data integrity, statistical sanity,
ML model quality, and drift detection.

---

## Project Structure
```
Tests/
├── phase4_data_testing.py    # Main test script
└── README.md
```

---

## Test Suites

### Suite 1 — Schema Validation
- Validates required columns exist in all 3 datasets
- Checks column data types match expected schema
- Covers Sales, Healthcare, and Finance datasets

### Suite 2 — Data Quality
- Null rate thresholds per dataset
- Duplicate row detection
- Range and domain constraint checks
- Referential integrity validation

### Suite 3 — Statistical Sanity
- Class balance checks
- Coefficient of variation (variance) checks
- Correlation direction validation

### Suite 4 — ML Model Sanity
- AUC > 0.65 threshold
- 5-fold cross-validation AUC > 0.60
- Overfitting gap < 0.10
- Both classes predicted
- No train/test data leakage

### Suite 5 — Data Drift Detection
- Normalised mean shift between baseline and new batch
- Covers income, credit score, loan amount

---

## Latest Test Results

| Metric | Result |
|--------|--------|
| Total Tests | 59 |
| ✅ Passed | 51 |
| ❌ Failed | 2 |
| ⚠️ Warnings | 6 |

### Failed Tests (expected — raw data issues fixed in Phase 1)
| Test | Detail |
|------|--------|
| `sales: no duplicate order_ids` | 20 dupes in raw data — removed in Phase 1 |
| `sales: quantity all positive` | 5 invalid rows in raw data — removed in Phase 1 |

### Warnings
| Warning | Detail |
|---------|--------|
| `sales dtype str vs object` | Pandas 3.x shows `str` instead of `object` — harmless |
| `healthcare: bmi outliers` | 4 outlier BMIs — handled in Phase 1 cleaning |

---

## Datasets Tested

| Dataset | Location | Rows | Columns |
|---------|----------|------|---------|
| Sales | `Sales-EDA/sales_data.csv` | 520 | 15 |
| Healthcare | `Healthcare-Visualization/healthcare_data.csv` | 800 | 22 |
| Finance | `Finance-ML/finance_data.csv` | 1000 | 20 |

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