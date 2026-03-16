# Data Science Portfolio — Japendra

Welcome to my Data Science Portfolio! This repository contains end-to-end data analysis projects showcasing data cleaning, EDA, visualizations, machine learning, production-grade testing, an interactive Streamlit dashboard, and SQL analytics using Python and MySQL.

---

## 🚀 Live Dashboard
👉 **[View Live Portfolio Dashboard](https://data-science-portfolio-25fwd289aynlntfxgs8rxm.streamlit.app)**

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
| Clean Data | 472 rows, 19 columns |
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

Production-grade automated testing framework covering all 3 datasets with 57 tests across 6 test suites. Generates visual HTML report and timestamped CSV results on every run.

| Item | Detail |
|------|--------|
| Total Tests | 57 |
| ✅ Passed | 55 |
| ❌ Failed | 2 (intentional — raw data issues documented) |
| ⚠️ Warnings | 0 |
| Tools | Python, Pandas, NumPy, Scikit-learn |
| Outputs | HTML visual report + CSV results history |

**Test Suites:**

| Suite | Tests | Status |
|-------|-------|--------|
| Suite 1 — Schema Validation | 23 | ✅ |
| Suite 2 — Raw Data Quality | 8 | ❌ (expected) |
| Suite 3 — Clean Data Quality | 11 | ✅ |
| Suite 4 — Statistical Sanity | 7 | ✅ |
| Suite 5 — ML Model Sanity | 5 | ✅ |
| Suite 6 — Drift Detection | 3 | ✅ |

---

### 5. 📱 Streamlit Portfolio Dashboard
**Folder:** `Streamlit-Dashboard/`

Interactive web dashboard covering all 3 projects with live charts, filters, KPI metrics, and a real-time loan default predictor.

| Item | Detail |
|------|--------|
| Pages | 4 (Home, Sales, Healthcare, Finance ML) |
| Tools | Python, Streamlit, Plotly, Scikit-learn |
| Features | Live filters, ML predictor, risk gauge, interactive charts |
| Run locally | `streamlit run app.py` |
| Live Demo | [Click here](https://data-science-portfolio-25fwd289aynlntfxgs8rxm.streamlit.app) |

**Key Features:**
- 📊 Interactive filters on every page
- 🤖 Real-time loan default prediction with risk gauge
- 📈 Plotly interactive charts
- 🏠 Portfolio overview with key metrics

---

### 6. 🗄️ SQL Analytics — Multi-Domain Database Project
**Folder:** `SQL-Analytics/`

Production-grade SQL project covering 4 business domains with 12 tables and 50+ queries demonstrating core to advanced SQL concepts using MySQL 8.0.

| Item | Detail |
|------|--------|
| Database | `portfolio_analytics` |
| Domains | E-Commerce, Healthcare, Finance, HR |
| Tables | 12 |
| Query Files | 6 |
| Total Queries | 50+ |
| Tools | MySQL 8.0 |

**SQL Concepts Covered:**

| File | Concept |
|------|---------|
| 01_basic_queries.sql | SELECT, WHERE, ORDER BY, LIMIT |
| 02_joins.sql | INNER, LEFT, SELF JOIN |
| 03_aggregations.sql | GROUP BY, HAVING, COUNT, SUM, AVG |
| 04_window_functions.sql | RANK, LAG, LEAD, OVER, PARTITION BY |
| 05_subqueries_ctes.sql | Subqueries, CTEs, CASE WHEN |
| 06_stored_procedures.sql | Stored procedures with IN/OUT params |

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
│   ├── test_report.html
│   ├── test_results.csv
│   └── README.md
│
├── Streamlit-Dashboard/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── SQL-Analytics/
│   ├── queries/
│   │   ├── 01_basic_queries.sql
│   │   ├── 02_joins.sql
│   │   ├── 03_aggregations.sql
│   │   ├── 04_window_functions.sql
│   │   ├── 05_subqueries_ctes.sql
│   │   └── 06_stored_procedures.sql
│   └── README.md
│
└── README.md
```

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.13+, SQL |
| Data Manipulation | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn |
| Dashboard | Streamlit |
| Database | MySQL 8.0 |
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
pip install numpy pandas matplotlib seaborn plotly scikit-learn streamlit

# Run Healthcare project
cd Healthcare-Visualization
python phase1_healthcare_eda.py
python phase2_healthcare_viz.py

# Run Sales project
cd ../Sales-EDA
python phase1_sales_eda.py
python phase2_sales_viz.py

# Run Finance ML project
cd ../Finance-ML
python phase1_finance_eda.py
python phase2_finance_viz.py
python phase3_finance_ml.py

# Run tests
cd ../Tests
python phase4_data_testing.py

# Run Streamlit dashboard
cd ../Streamlit-Dashboard
streamlit run app.py

# Run SQL queries (MySQL)
mysql -u root -p
SOURCE queries/01_basic_queries.sql;
```

---

## Author
**Japendra**
Data Scientist | Python | SQL | Pandas | Data Visualization | Machine Learning
📁 [GitHub Portfolio](https://github.com/Reddy062023/Data-Science-Portfolio)
🚀 [Live Dashboard](https://data-science-portfolio-25fwd289aynlntfxgs8rxm.streamlit.app)