# Data Science Portfolio — Japendra

Welcome to my Data Science Portfolio! This repository contains end-to-end data analysis projects showcasing data cleaning, EDA, visualizations, and business insights using Python.

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
└── README.md
```

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.13+ |
| Data Manipulation | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Environment | Anaconda, VS Code |
| Version Control | Git, GitHub |

---

## Setup
```bash
# Clone the repo
git clone https://github.com/Reddy062023/Data-Science-Portfolio.git

# Navigate to any project
cd Healthcare-Visualization

# Activate environment
conda activate myenv

# Install dependencies
pip install numpy pandas matplotlib seaborn plotly

# Run analysis
python phase1_healthcare_eda.py
python phase2_healthcare_viz.py
```

---

## Author
**Japendra**  
Data Scientist | Python | Pandas | Data Visualization  
📁 [GitHub Portfolio](https://github.com/Reddy062023/Data-Science-Portfolio)