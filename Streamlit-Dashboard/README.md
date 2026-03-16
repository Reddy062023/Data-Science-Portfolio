# Streamlit Portfolio Dashboard

## Overview
Interactive web dashboard built with Streamlit covering all 3 data science projects.
Features live charts, filters, KPI metrics, and a real-time loan default predictor powered by Machine Learning.

---

## Project Structure
```
Streamlit-Dashboard/
├── app.py                # Main dashboard application
├── requirements.txt      # Dependencies
└── README.md
```

---

## Pages

### 🏠 Home
- Portfolio overview
- Key metrics (total projects, rows analyzed, models built, charts)
- Project summaries for all 3 datasets

### 📊 Sales Analytics
- Filter by Region, Channel, Product
- Monthly revenue trend (line chart)
- Revenue by region (pie chart)
- Top 10 products by revenue (bar chart)
- Revenue by channel (bar chart)
- Sales rep leaderboard (table)

### 🏥 Healthcare Analytics
- Filter by Gender, Diagnosis, Insurance Type
- Diagnosis distribution (pie chart)
- Readmission rate by insurance (bar chart)
- BMI vs Systolic BP scatter plot
- Hospital days by diagnosis (box plot)
- Clinical metrics summary table

### 💰 Finance ML
- Filter by Loan Grade, Loan Purpose, Employment Status
- Default rate by loan grade (bar chart)
- Credit score distribution (histogram)
- Default rate by loan purpose (bar chart)
- Debt-to-income vs credit score (scatter)
- **🤖 Live Loan Default Predictor** — enter customer details and get instant prediction with risk gauge

---

## Key Features
- ✅ Interactive filters on every page
- ✅ Real-time ML prediction with risk gauge
- ✅ Plotly interactive charts
- ✅ Cached data loading for performance
- ✅ Responsive layout

---

## Setup & Usage

### 1. Activate your environment
```bash
conda activate myenv
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
cd Streamlit-Dashboard
streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## Requirements
| Package | Version |
|---------|---------|
| Python | 3.13+ |
| streamlit | latest |
| pandas | latest |
| numpy | latest |
| plotly | latest |
| scikit-learn | latest |

---

## Author
**Japendra**
Data Analysis Portfolio — Streamlit Dashboard