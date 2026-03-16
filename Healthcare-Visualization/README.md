# Healthcare Data — Exploratory Data Analysis & Visualization

## Overview
End-to-end Healthcare Data Analysis (800 rows, 22 columns) from a Senior Data Scientist perspective.  
Covers data profiling, quality checks, cleaning, feature engineering, clinical insights, and visualizations.

---

## Project Structure
```
Healthcare-Visualization/
│
├── healthcare_data.csv              # Raw input data (800 rows, 22 columns)
├── healthcare_data_clean.csv        # Cleaned output (770 rows, 26 columns)
├── phase1_healthcare_eda.py         # Phase 1 — EDA & Cleaning
├── phase2_healthcare_viz.py         # Phase 2 — Visualizations
├── plots/                           # All saved charts
│   ├── chart1_population_overview.png
│   ├── chart2_correlation.png
│   └── chart3_risk_factors.png
└── README.md
```

---

## Phase 1 — EDA & Cleaning

### Step 1 — Load & First Look
- Loads `healthcare_data.csv` — 800 rows, 22 columns
- Prints shape, column dtypes, and first 5 rows

### Step 2 — Automated Data Profile
- Reusable `profile_dataframe()` function
- Reports nulls, unique values, dtypes, and sample values per column
- Identified nulls in `bmi` (30), `cholesterol_total` (15), `glucose_level` (20)

### Step 3 — Data Quality & Cleaning
- No duplicate `patient_id` rows found
- Drops rows with invalid age, BMI, or blood pressure
- Fills numeric nulls with median (BMI, glucose, cholesterol, BP)
- Fills categorical nulls for smoker, diabetic, gender, insurance, diagnosis
- Final clean shape: **770 rows × 26 columns**

### Step 4 — Feature Engineering
- `age_group` — binned into <18, 18-35, 35-50, 50-65, 65+
- `bmi_category` — Underweight / Normal / Overweight / Obese
- `bp_category` — Normal / Elevated / High Stage 1 / High Stage 2
- `high_risk` — flag for patients with 1+ clinical risk factors

### Step 5 — Business Insights
- Patient demographics (age, gender, insurance type)
- Clinical metrics (BMI, BP, cholesterol, glucose)
- Diagnosis breakdown with avg age, BMI, BP, hospital days
- 30-day readmission analysis by diagnosis, insurance, age group
- Smoking & diabetes risk and critical diagnosis rates
- Hospital stay analysis by diagnosis and age group

### Export
- Cleaned data saved as `healthcare_data_clean.csv` in the same folder

---

## Phase 2 — Visualizations

| # | Chart | Description |
|---|-------|-------------|
| 1 | Patient Population Overview | Age distribution, BMI vs BP scatter, diagnosis donut, readmission by insurance, cholesterol violin, hospital stay box |
| 2 | Correlation Heatmap | Feature correlation matrix across 10 clinical variables |
| 3 | Risk Factor Analysis | Diagnosis by gender, critical rate by age group, diagnosis by exercise level |

All charts saved to `plots/` as `.png`.

---

## Key Insights from Data

| Metric | Value |
|--------|-------|
| Total Patients (clean) | 770 |
| Avg Age | 52.5 years |
| Overall 30-day Readmission Rate | 20.9% |
| High Risk Patients | 78.2% |
| Smoker Rate | 22.9% |
| Diabetic Rate | 15.1% |
| Critical — Smokers vs Non-Smokers | 9.1% vs 4.5% |
| Critical — Diabetic vs Non-Diabetic | 13.8% vs 4.1% |
| Avg Hospital Days | 10.0 |
| Highest Readmission by Insurance | Medicaid (26.5%) |
| Highest Readmission by Age Group | 50-65 yrs (29.5%) |

---

## Diagnosis Breakdown

| Diagnosis | Patients | Share | Avg Age | Avg BMI | Avg BP |
|-----------|----------|-------|---------|---------|--------|
| At Risk   | 681      | 88.4% | 52.5    | 27.1    | 135.5  |
| Healthy   | 46       | 6.0%  | 29.5    | 23.3    | 111.5  |
| Critical  | 43       | 5.6%  | 76.0    | 30.5    | 163.0  |

---

## Setup & Usage

### 1. Activate your environment
```bash
conda activate myenv
```

### 2. Install dependencies
```bash
pip install numpy pandas matplotlib seaborn
```

### 3. Run Phase 1 — EDA
```bash
python phase1_healthcare_eda.py
```

### 4. Run Phase 2 — Visualizations
```bash
python phase2_healthcare_viz.py
```

---

## Requirements
| Package    | Version |
|------------|---------|
| Python     | 3.13+   |
| pandas     | latest  |
| numpy      | latest  |
| matplotlib | latest  |
| seaborn    | latest  |

---

## Author
Japendra  
Data Analysis Portfolio — Healthcare Visualization Project