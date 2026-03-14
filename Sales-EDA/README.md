<<<<<<< HEAD
# Healthcare Data Visualization — Phase 2

## Overview
This project demonstrates exploratory data visualization on a healthcare dataset containing **800 patients and 22 features**. The focus is on **patient demographics, risk factors, and clinical insights**. Charts are designed with professional styling and storytelling suitable for data-driven decision-making.

## Tools & Libraries
- **Python**: pandas, numpy  
- **Visualization**: matplotlib, seaborn, gridspec  
- **Data Cleaning & Analysis**: Handling missing values, aggregation, crosstabs

## Dataset
- **File**: `healthcare_data.csv`  
- **Key Features**: `age`, `bmi`, `blood_pressure_systolic`, `cholesterol_total`, `glucose_level`, `hospital_days`, `readmitted_30d`, `diagnosis`, `smoker`, `diabetic`, `exercise_hrs_week`  

> Note: The dataset is anonymized and suitable for educational purposes.

## Key Visualizations

### 1️⃣ Patient Population Overview (2x3 Grid)
- Age distribution by diagnosis
- BMI vs Systolic Blood Pressure (scatter)
- Diagnosis distribution (pie chart)
- 30-day readmission rate by insurance type
- Cholesterol distribution by smoking status
- Hospital stay length by diagnosis

![Population Overview](chart1_population_overview.png)

---

### 2️⃣ Correlation Heatmap
- Shows correlations between numeric features (e.g., BMI, blood pressure, cholesterol)
- Helps identify multicollinearity and relationships between risk factors

![Correlation Heatmap](chart2_correlation.png)

---

### 3️⃣ Risk Factor Analysis
- Diagnosis mix by gender (stacked bar chart)
- Critical diagnosis rate by age group
- Diagnosis distribution by weekly exercise hours

![Risk Factor Analysis](chart3_risk_factors.png)

---

## Key Insights
- **Readmission Rate**: XX% overall
- **Hospital Stay**: Critical patients stay longer on average
- **Risk Factors**:
  - Smokers and diabetics have a higher critical diagnosis rate
  - Low exercise hours correlate with higher critical diagnosis percentage
  - Age and gender differences affect diagnosis mix

---

## How to Run
```bash
python phase2_healthcare_viz.py
=======
# Sales Data EDA Project

**Project Goal:** Perform exploratory data analysis and cleaning on sales dataset.

**Dataset:** sales_data.csv (520 rows × 15 columns)

**Steps performed:**
- Data loading and inspection
- Null value and duplicate handling
- Feature engineering (revenue, ship_days, month, quarter)
- Business insights: top products, revenue by region/channel, return rates

**Files included:**
- `sales_data.csv` — original dataset
- `sales_data_clean.csv` — cleaned dataset
- `phase1_sales_eda.py` — Python script
- `plots/` — optional folder for charts

**GitHub Link:** [Add your repo link here]
>>>>>>> e393e20c5cd8d8899672a97e4053f0ae5706b503
