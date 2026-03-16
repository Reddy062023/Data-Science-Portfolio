"""
Phase 2: Visualization — Healthcare Data
Approach: Senior Lead / Data Scientist perspective
Dataset: healthcare_data_clean.csv (output from Phase 1)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")

# ─── Professional chart theme ────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "#f8f9fa",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":       "sans-serif",
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
})

# ─── Paths ───────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent
PLOTS_DIR = BASE_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

# ─── Load clean dataset ──────────────────────────────────────────
df = pd.read_csv(BASE_DIR / "healthcare_data_clean.csv")

# ─── Restore engineered columns if missing ───────────────────────
if "age_group" not in df.columns:
    df["age_group"] = pd.cut(
        df["age"], bins=[0, 18, 35, 50, 65, 120],
        labels=["<18", "18-35", "35-50", "50-65", "65+"]
    )

if "high_risk" not in df.columns:
    df["high_risk"] = (
        (df["smoker"] == 1) |
        (df["diabetic"] == 1) |
        (df["bmi"] >= 30) |
        (df["blood_pressure_systolic"] >= 140)
    ).astype(int)

print(f"Loaded: {df.shape[0]} patients, {df.shape[1]} features")
print(f"Diagnosis breakdown:\n{df['diagnosis'].value_counts()}")

diagnosis_order = ["Healthy", "At Risk", "Critical"]
palette = {"Healthy": "#2ecc71", "At Risk": "#f39c12", "Critical": "#e74c3c"}

# ───────────────────────────────────────────────────────────────
# CHART 1 — Patient Population Overview (2x3 grid)
# ───────────────────────────────────────────────────────────────
print("\n[1] Patient Population Overview")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Patient Population Overview — Healthcare Dataset",
             fontsize=15, fontweight="bold", y=1.01)

for diag in diagnosis_order:
    subset = df[df["diagnosis"] == diag]["age"]
    axes[0,0].hist(subset, bins=20, alpha=0.65, label=diag, color=palette[diag])
axes[0,0].set_title("Age Distribution by Diagnosis")
axes[0,0].set_xlabel("Age")
axes[0,0].set_ylabel("Patient Count")
axes[0,0].legend()

for diag in diagnosis_order:
    sub = df[df["diagnosis"] == diag]
    axes[0,1].scatter(sub["bmi"], sub["blood_pressure_systolic"],
                      alpha=0.4, s=20, label=diag, color=palette[diag])
axes[0,1].set_title("BMI vs Systolic Blood Pressure")
axes[0,1].set_xlabel("BMI")
axes[0,1].set_ylabel("Systolic BP (mmHg)")
axes[0,1].axvline(25, color="gray", linestyle="--", alpha=0.5, label="BMI=25")
axes[0,1].axvline(30, color="orange", linestyle="--", alpha=0.5, label="BMI=30")
axes[0,1].legend(fontsize=8)

counts = df["diagnosis"].value_counts()[diagnosis_order]
wedge_props = dict(width=0.55)
axes[0,2].pie(counts, labels=counts.index, autopct="%1.1f%%",
              colors=[palette[d] for d in counts.index],
              wedgeprops=wedge_props, startangle=90)
axes[0,2].set_title("Diagnosis Distribution")

readmit = df.groupby("insurance_type")["readmitted_30d"].mean() * 100
readmit = readmit.sort_values(ascending=True)
bars = axes[1,0].barh(readmit.index, readmit.values, color="#4a90d9", height=0.5)
axes[1,0].set_title("30-Day Readmission Rate by Insurance")
axes[1,0].set_xlabel("Readmission Rate (%)")
for bar, val in zip(bars, readmit.values):
    axes[1,0].text(val + 0.3, bar.get_y() + bar.get_height()/2,
                   f"{val:.1f}%", va="center", fontsize=9)

sns.violinplot(data=df, x="smoker", y="cholesterol_total", ax=axes[1,1],
               palette=["#2ecc71","#e74c3c"])
axes[1,1].set_xticklabels(["Non-Smoker","Smoker"])
axes[1,1].set_title("Cholesterol Distribution by Smoking Status")
axes[1,1].set_ylabel("Total Cholesterol (mg/dL)")

sns.boxplot(data=df, x="diagnosis", y="hospital_days", ax=axes[1,2],
            order=diagnosis_order, palette=palette, width=0.5, fliersize=3)
axes[1,2].set_title("Hospital Stay Length by Diagnosis")
axes[1,2].set_ylabel("Days")
axes[1,2].set_xlabel("")

plt.tight_layout()
chart1_path = PLOTS_DIR / "chart1_population_overview.png"
plt.savefig(chart1_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  ✓ Saved → {chart1_path.name}")

# ───────────────────────────────────────────────────────────────
# CHART 2 — Correlation Heatmap
# ───────────────────────────────────────────────────────────────
print("\n[2] Correlation Heatmap")

numeric_cols = ["age","bmi","blood_pressure_systolic","blood_pressure_diastolic",
                "cholesterol_total","glucose_level","hospital_days",
                "num_visits_year","medication_count","exercise_hrs_week"]

corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(12, 9))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn",
            center=0, square=True, linewidths=0.5, ax=ax,
            annot_kws={"size": 9})
ax.set_title("Feature Correlation Matrix — Healthcare",
             fontsize=14, fontweight="bold", pad=20)
plt.tight_layout()
chart2_path = PLOTS_DIR / "chart2_correlation.png"
plt.savefig(chart2_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  ✓ Saved → {chart2_path.name}")

# ───────────────────────────────────────────────────────────────
# CHART 3 — Risk Factor Analysis
# ───────────────────────────────────────────────────────────────
print("\n[3] Risk Factor Analysis")

fig = plt.figure(figsize=(16, 6))
gs  = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)

ax1   = fig.add_subplot(gs[0])
cross = pd.crosstab(df["gender"], df["diagnosis"], normalize="index") * 100
cross[diagnosis_order].plot(kind="bar", ax=ax1, stacked=True,
                            color=[palette[d] for d in diagnosis_order],
                            edgecolor="white", linewidth=0.5)
ax1.set_title("Diagnosis Mix by Gender")
ax1.set_ylabel("% of Gender Group")
ax1.set_xlabel("")
ax1.tick_params(axis="x", rotation=0)
ax1.legend(title="Diagnosis", fontsize=8)

crit_rate = df.groupby("age_group", observed=True).apply(
    lambda g: (g["diagnosis"] == "Critical").mean() * 100
).reset_index()
crit_rate.columns = ["age_group", "critical_rate"]

ax2  = fig.add_subplot(gs[1])
bars = ax2.bar(crit_rate["age_group"], crit_rate["critical_rate"],
               color="#e74c3c", alpha=0.8, width=0.5)
ax2.set_title("Critical Diagnosis Rate by Age Group")
ax2.set_ylabel("% Classified as Critical")
ax2.set_xlabel("Age Group")
for bar, val in zip(bars, crit_rate["critical_rate"]):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{val:.1f}%", ha="center", fontsize=9)

df["exercise_bin"] = pd.cut(df["exercise_hrs_week"], bins=[0,1,3,5,30],
                             labels=["0-1h","1-3h","3-5h","5h+"])
ex_diag = pd.crosstab(df["exercise_bin"], df["diagnosis"], normalize="index") * 100

ax3  = fig.add_subplot(gs[2])
ex_diag[diagnosis_order].plot(kind="bar", ax=ax3, stacked=True,
                               color=[palette[d] for d in diagnosis_order],
                               edgecolor="white", linewidth=0.5)
ax3.set_title("Diagnosis Mix by Weekly Exercise")
ax3.set_ylabel("% of Exercise Group")
ax3.set_xlabel("Hours / Week")
ax3.tick_params(axis="x", rotation=0)
ax3.legend(title="Diagnosis", fontsize=8)

fig.suptitle("Risk Factor Analysis — Key Insights for Clinical Review",
             fontsize=14, fontweight="bold", y=1.02)
chart3_path = PLOTS_DIR / "chart3_risk_factors.png"
plt.savefig(chart3_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  ✓ Saved → {chart3_path.name}")

# ─── Quick insight summary ────────────────────────────────────────
print("\n" + "=" * 60)
print("KEY INSIGHTS")
print("=" * 60)
print(f"Readmission overall:          {df['readmitted_30d'].mean()*100:.1f}%")
print(f"Avg hospital days (Critical): {df[df['diagnosis']=='Critical']['hospital_days'].mean():.1f}")
print(f"Smoker critical rate:         {(df[df['smoker']==1]['diagnosis']=='Critical').mean()*100:.1f}%")
print(f"Non-smoker critical:          {(df[df['smoker']==0]['diagnosis']=='Critical').mean()*100:.1f}%")
print(f"Diabetic critical rate:       {(df[df['diabetic']==1]['diagnosis']=='Critical').mean()*100:.1f}%")

print("\n✓ Phase 2 complete. 3 charts saved in plots/ folder.")