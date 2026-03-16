# Healthcare Data — Exploratory Data Analysis & Visualization

## Overview
End-to-end Healthcare Data Analysis (800 rows, 22 columns) from a Senior Data Scientist perspective.  
Covers data profiling, quality checks, cleaning, feature engineering, clinical insights, and visualizations.

---

## Project Structure
```
Healthcare-Visualization/
│
├── healthcare_data.csv              # Raw input data
├── healthcare_data_clean.csv        # Cleaned output (auto-generated)
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
- Loads `healthcare_data.csv` (800 rows, 22 columns)
- Prints shape, column dtypes, and first 5 rows

### Step 2 — Automated Data Profile
- Reusable `profile_dataframe()` function
- Reports nulls, unique values, dtypes, and sample values per column

### Step 3 — Data Quality & Cleaning
- Removes duplicate `patient_id` rows
- Drops rows with invalid age, BMI, or blood pressure
- Fills numeric nulls with median (BMI, glucose, cholesterol, BP)
- Fills categorical nulls for smoker, diabetic, gender, insurance, diagnosis

### Step 4 — Feature Engineering
- `age_group` — binned age categories (<18, 18-35, 35-50, 50-65, 65+)
- `bmi_category` — Underweight / Normal / Overweight / Obese
- `bp_category` — Normal / Elevated / High Stage 1 / High Stage 2
- `high_risk` — flag for patients with 1+ risk factors

### Step 5 — Business Insights
- Patient demographics (age, gender, insurance)
- Clinical metrics (BMI, BP, cholesterol, glucose)
- Diagnosis breakdown with avg age, BMI, BP, hospital days
- 30-day readmission analysis by diagnosis, insurance, age group
- Smoking & diabetes risk rates and critical diagnosis rates
- Hospital stay analysis by diagnosis and age group

### Export
- Cleaned data saved as `healthcare_data_clean.csv` in the same folder

---

## Phase 2 — Visualizations

| # | Chart | Description |
|---|-------|-------------|
| 1 | Patient Population Overview | Age distribution, BMI vs BP scatter, diagnosis pie, readmission by insurance, cholesterol violin, hospital stay box |
| 2 | Correlation Heatmap | Feature correlation matrix across 10 clinical variables |
| 3 | Risk Factor Analysis | Diagnosis by gender, critical rate by age group, diagnosis by exercise level |

All charts saved to `plots/` folder as `.png`.

---

## Key Insights
- Overall 30-day readmission rate: **20.9%**
- Critical patients avg age: **76 years**
- Smoker critical diagnosis rate: **9.1%** vs Non-smoker: **4.5%**
- Diabetic critical diagnosis rate: **13.8%** vs Non-diabetic: **4.1%**
- High risk patients: **78.2%** of total population

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
Geetu  
Data Analysis Portfolio — Healthcare Visualization Project