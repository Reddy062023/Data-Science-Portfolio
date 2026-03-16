# Data Science Portfolio — Japendra

Welcome to my Data Science Portfolio! This repository contains end-to-end data analysis projects showcasing data cleaning, EDA, visualizations, machine learning, and production-grade data testing using Python.

---

## Projects

### 1. 🏥 Healthcare Data — EDA & Visualization
**Folder:** `Healthcare-Visualization/`

Analysis of 800 patient records covering clinical metrics, diagnosis breakdown, risk factors, and readmission rates.

| Item | Detail |
|------|--------|
| Dataset | 800 rows, 22 columns |
| Clean Data | 770 rows, 26 columns |
| Tools | Python, Pandas, NumPy, Matplotlib, Seaborn |
| Charts | 3 (Population Overview, Correlation Heatmap, Risk Factors) |

**Key Findings:**
- Overall 30-day readmission rate: **20.9%**
- Diabetic patients have **3x higher** critical diagnosis rate
- Patients aged 50-65 have the highest readmission rate at **29.5%**
- High risk patients make up **78.2%** of the population

---

### 2. 📊 Sales Data — EDA & Visualization
**Folder:** `Sales-EDA/`

Analysis of 520 sales transactions covering revenue trends, product performance, regional analysis, and sales rep leaderboard.

| Item | Detail |
|------|--------|
| Dataset | 520 rows, 15 columns |
| Tools | Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly |
| Charts | 12 (6 static + 6 interactive) |

**Key Findings:**
- Revenue breakdown across 4 channels — Direct Sales leads
- Top products and regions identified by revenue share
- Sales rep leaderboard with avg order value analysis
- Interactive HTML charts for stakeholder sharing

---

### 3. 💰 Finance ML — Loan Default Prediction
**Folder:** `Finance-ML/`

End-to-end ML pipeline on 1000 loan records to predict default risk using Logistic Regression, Random Forest, and Gradient Boosting.

| Item | Detail |
|------|--------|
| Dataset | 1000 rows, 20 columns |
| Clean Data | 960 rows, 29 columns |
| Tools | Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Scikit-learn |
| Charts | 15 (7 static + 7 interactive + 1 ML evaluation) |
| Models | Logistic Regression, Random Forest, Gradient Boosting |

**Key Findings:**
- Overall loan default rate: **37.5%**
- Credit score and debt-to-income are top predictors
- Gradient Boosting achieved highest AUC score
- Late payments and loan grade are strong risk indicators

---

### 4. 🧪 Data Testing & Validation Framework
**Folder:** `Tests/`

Production-grade automated testing framework covering all 3 datasets with 59 tests across 5 test suites.

| Item | Detail |
|------|--------|
| Total Tests | 59 |
| Passed | 51 |
| Failed | 2 (expected — raw data issues fixed in Phase 1) |
| Warnings | 6 (harmless) |
| Tools | Python, Pandas, NumPy, Scikit-learn |

**Test Suites:**
- Suite 1 — Schema Validation
- Suite 2 — Data Quality
- Suite 3 — Statistical Sanity
- Suite 4 — ML Model Sanity
- Suite 5 — Data Drift Detection

---

## Repository Structure
```
Data-Science-Portfolio/
│
├── Healthcare-Visualization/
│   ├── healthcare_data.csv
│   ├── healthcare_data_clean.csv
│   ├── phase1_healthcare_eda.py
│   ├── phase2_healthcare_viz.py
│   ├── plots/
│   └── README.md
│
├── Sales-EDA/
│   ├── sales_data.csv
│   ├── sales_data_clean.csv
│   ├── phase1_sales_eda.py
│   ├── phase2_sales_viz.py
│   ├── plots/
│   └── README.md
│
├── Finance-ML/
│   ├── finance_data.csv
│   ├── finance_data_clean.csv
│   ├── phase1_finance_eda.py
│   ├── phase2_finance_viz.py
│   ├── phase3_finance_ml.py
│   ├── plots/
│   └── README.md
│
├── Tests/
│   ├── phase4_data_testing.py
│   └── README.md
│
└── README.md
```

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.13+ |
| Data Manipulation | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn |
| Testing | Custom TestRunner Framework |
| Environment | Anaconda, VS Code |
| Version Control | Git, GitHub |

---

## Setup
```bash
# Clone the repo
git clone https://github.com/Reddy062023/Data-Science-Portfolio.git

# Activate environment
conda activate myenv

# Install dependencies
pip install numpy pandas matplotlib seaborn plotly scikit-learn

# Run any project
cd Healthcare-Visualization
python phase1_healthcare_eda.py
python phase2_healthcare_viz.py

cd ../Sales-EDA
python phase1_sales_eda.py
python phase2_sales_viz.py

cd ../Finance-ML
python phase1_finance_eda.py
python phase2_finance_viz.py
python phase3_finance_ml.py

# Run tests
cd ../Tests
python phase4_data_testing.py
```

---

## Author
**Japendra**
Data Scientist | Python | Pandas | Data Visualization | Machine Learning
📁 [GitHub Portfolio](https://github.com/Reddy062023/Data-Science-Portfolio)