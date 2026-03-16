# Finance ML — Loan Default Prediction

## Overview
End-to-end Machine Learning pipeline on a Finance / Loan dataset (1000 rows, 20 columns) from a Senior Data Scientist perspective.
Covers data profiling, cleaning, feature engineering, visualizations, and a production-grade ML pipeline with 3 models.

---

## Project Structure
```
Finance-ML/
│
├── finance_data.csv              # Raw input data (1000 rows, 20 columns)
├── finance_data_clean.csv        # Cleaned output (960 rows, 29 columns)
├── phase1_finance_eda.py         # Phase 1 — EDA & Cleaning
├── phase2_finance_viz.py         # Phase 2 — Visualizations
├── phase3_finance_ml.py          # Phase 3 — ML Pipeline
├── plots/                        # All saved charts
│   ├── chart1_default_rate_loan_grade.png
│   ├── chart1_default_rate_loan_grade_interactive.html
│   ├── chart2_default_rate_income_tier.png
│   ├── chart2_default_rate_income_tier_interactive.html
│   ├── chart3_loan_amount_distribution.png
│   ├── chart3_loan_amount_distribution_interactive.html
│   ├── chart4_credit_score_distribution.png
│   ├── chart4_credit_score_distribution_interactive.html
│   ├── chart5_debt_to_income_analysis.png
│   ├── chart5_debt_to_income_analysis_interactive.html
│   ├── chart6_default_rate_loan_purpose.png
│   ├── chart6_default_rate_loan_purpose_interactive.html
│   ├── chart7_correlation_heatmap.png
│   ├── chart7_correlation_heatmap_interactive.html
│   └── chart8_ml_evaluation.png
└── README.md
```

---

## Phase 1 — EDA & Cleaning

### Step 1 — Load & First Look
- Loads `finance_data.csv` — 1000 rows, 20 columns
- Prints shape, column dtypes, and first 5 rows

### Step 2 — Automated Data Profile
- Reusable `profile_dataframe()` function
- Reports nulls, unique values, dtypes, and sample values per column

### Step 3 — Data Quality & Cleaning
- Removes duplicate rows
- Drops rows with invalid income, loan amount, age, credit score
- Fills numeric nulls with median
- Fills categorical nulls with Unknown
- Final clean shape: **960 rows × 29 columns**

### Step 4 — Feature Engineering
- `debt_to_income` — loan amount / annual income
- `monthly_payment` — loan amount / term months
- `payment_to_income` — monthly payment / monthly income
- `total_debt_ratio` — total debt / annual income
- `interest_cost_total` — total interest over loan term
- `risk_per_year` — late payments per year
- `credit_tier` — Very Poor / Fair / Good / Very Good / Excellent
- `income_tier` — Low / Lower-Mid / Mid / Upper-Mid / High
- `loan_size` — Small / Medium / Large / Very Large

### Export
- Cleaned data saved as `finance_data_clean.csv` in same folder

---

## Phase 2 — Visualizations

| # | Chart | Description |
|---|-------|-------------|
| 1 | Default Rate by Loan Grade | Bar chart with avg line |
| 2 | Default Rate by Income Tier | Bar + borrower count chart |
| 3 | Loan Amount Distribution | Histogram + box by loan size |
| 4 | Credit Score Distribution | Histogram + default rate by tier |
| 5 | Debt-to-Income Analysis | Violin + scatter vs credit score |
| 6 | Default Rate by Loan Purpose | Horizontal bar chart |
| 7 | Correlation Heatmap | 12 feature correlation matrix |

All charts saved as `.png` (static) and `.html` (interactive).

---

## Phase 3 — Machine Learning

### Models Trained
| Model | Type |
|-------|------|
| Logistic Regression | Baseline linear model |
| Random Forest | Ensemble tree model |
| Gradient Boosting | Boosted tree model |

### Pipeline
- Numeric features: median imputation + standard scaling
- Categorical features: label encoding + most frequent imputation
- 5-fold stratified cross validation
- 80/20 train/test split

### Evaluation Metrics
- ROC-AUC score
- Average Precision score
- Classification report
- Confusion matrix
- Permutation feature importance

### Chart Saved
- `chart8_ml_evaluation.png` — ROC curves, PR curves, confusion matrix, top 12 features

---

## Setup & Usage

### 1. Activate your environment
```bash
conda activate myenv
```

### 2. Install dependencies
```bash
pip install numpy pandas matplotlib seaborn plotly scikit-learn
```

### 3. Run Phase 1 — EDA
```bash
python phase1_finance_eda.py
```

### 4. Run Phase 2 — Visualizations
```bash
python phase2_finance_viz.py
```

### 5. Run Phase 3 — ML Pipeline
```bash
python phase3_finance_ml.py
```

---

## Requirements
| Package | Version |
|---------|---------|
| Python | 3.13+ |
| pandas | latest |
| numpy | latest |
| matplotlib | latest |
| seaborn | latest |
| plotly | latest |
| scikit-learn | latest |

---

## Author
**Japendra**
Data Analysis Portfolio — Finance ML Project