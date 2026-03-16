# Data Science Portfolio — Japendra

Welcome to my Data Science Portfolio! This repository contains end-to-end data analysis projects showcasing data cleaning, EDA, visualizations, and machine learning using Python.

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
| Environment | Anaconda, VS Code |
| Version Control | Git, GitHub |

---

## Setup
```bash
# Clone the repo
git clone https://github.com/Reddy062023/Data-Science-Portfolio.git

# Navigate to any project
cd Finance-ML

# Activate environment
conda activate myenv

# Install dependencies
pip install numpy pandas matplotlib seaborn plotly scikit-learn

# Run analysis
python phase1_finance_eda.py
python phase2_finance_viz.py
python phase3_finance_ml.py
```

---

## Author
**Japendra**
Data Scientist | Python | Pandas | Data Visualization | Machine Learning
📁 [GitHub Portfolio](https://github.com/Reddy062023/Data-Science-Portfolio)