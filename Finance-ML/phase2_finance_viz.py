"""
Phase 2: Visualizations — Finance / Loan Default Data
Approach: Senior Lead / Data Scientist perspective
Dataset: finance_data_clean.csv (output from Phase 1)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go

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

FIG_DPI = 150

# ─── Load clean dataset ──────────────────────────────────────────
df = pd.read_csv(BASE_DIR / "finance_data_clean.csv")

# ─── Fix dtypes ──────────────────────────────────────────────────
df["defaulted"] = df["defaulted"].astype(int)

# ─── Restore engineered columns if missing ───────────────────────
if "credit_tier" not in df.columns:
    df["credit_tier"] = pd.cut(
        df["credit_score"],
        bins=[0, 549, 649, 699, 749, 850],
        labels=["Very Poor", "Fair", "Good", "Very Good", "Excellent"]
    )

if "income_tier" not in df.columns:
    df["income_tier"] = pd.cut(
        df["income_annual"],
        bins=[0, 30000, 60000, 100000, 200000, 99999999],
        labels=["Low", "Lower-Mid", "Mid", "Upper-Mid", "High"]
    )

if "loan_size" not in df.columns:
    df["loan_size"] = pd.cut(
        df["loan_amount"],
        bins=[0, 5000, 15000, 30000, 99999999],
        labels=["Small", "Medium", "Large", "Very Large"]
    )

if "debt_to_income" not in df.columns:
    df["debt_to_income"] = (df["loan_amount"] / df["income_annual"]).round(4)

print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} cols")
print(f"Default rate: {df['defaulted'].mean()*100:.1f}%")

def save_fig(fig, name, kind="mpl"):
    path = PLOTS_DIR / f"{name}.{'html' if kind == 'plotly' else 'png'}"
    if kind == "plotly":
        fig.write_html(str(path))
    else:
        fig.savefig(path, dpi=FIG_DPI, bbox_inches="tight")
        plt.close(fig)
    print(f"  ✓ Saved → {path.name}")

# ─────────────────────────────────────────────────────────────────
# CHART 1 — Default Rate by Loan Grade
# ─────────────────────────────────────────────────────────────────
print("\n[1] Default Rate by Loan Grade")

loan_grade_default = (
    df.groupby("loan_grade")["defaulted"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False)
    .reset_index()
)
loan_grade_default.columns = ["loan_grade", "default_rate"]

# --- Seaborn ---
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#e74c3c" if r > df["defaulted"].mean() * 100
          else "#2ecc71" for r in loan_grade_default["default_rate"]]
bars = ax.bar(loan_grade_default["loan_grade"],
              loan_grade_default["default_rate"],
              color=colors, alpha=0.85, width=0.5)
ax.axhline(df["defaulted"].mean() * 100, color="gray", linestyle="--",
           linewidth=1.5, label=f'Avg: {df["defaulted"].mean()*100:.1f}%')
ax.set_title("Default Rate by Loan Grade", fontsize=15, fontweight="bold")
ax.set_xlabel("Loan Grade")
ax.set_ylabel("Default Rate (%)")
ax.legend()
for bar, val in zip(bars, loan_grade_default["default_rate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{val:.1f}%", ha="center", fontsize=9)
save_fig(fig, "chart1_default_rate_loan_grade")

# --- Plotly ---
fig_px = px.bar(
    loan_grade_default, x="loan_grade", y="default_rate",
    title="Default Rate by Loan Grade",
    labels={"loan_grade": "Loan Grade", "default_rate": "Default Rate (%)"},
    color="default_rate", color_continuous_scale=["#2ecc71", "#e74c3c"],
    template="plotly_white"
)
save_fig(fig_px, "chart1_default_rate_loan_grade_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# CHART 2 — Default Rate by Income Tier
# ─────────────────────────────────────────────────────────────────
print("\n[2] Default Rate by Income Tier")

income_default = (
    df.groupby("income_tier", observed=True)["defaulted"]
    .agg(default_rate=lambda x: x.mean() * 100,
         count="count")
    .round(2)
    .reset_index()
)

# --- Seaborn ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

bars = axes[0].bar(income_default["income_tier"],
                   income_default["default_rate"],
                   color="#4a90d9", alpha=0.85, width=0.5)
axes[0].axhline(df["defaulted"].mean() * 100, color="red", linestyle="--",
                linewidth=1.5, label=f'Avg: {df["defaulted"].mean()*100:.1f}%')
axes[0].set_title("Default Rate by Income Tier", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Income Tier")
axes[0].set_ylabel("Default Rate (%)")
axes[0].legend()
for bar, val in zip(bars, income_default["default_rate"]):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f"{val:.1f}%", ha="center", fontsize=9)

axes[1].bar(income_default["income_tier"], income_default["count"],
            color="#2ecc71", alpha=0.85, width=0.5)
axes[1].set_title("Borrower Count by Income Tier", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Income Tier")
axes[1].set_ylabel("Number of Borrowers")
for bar, val in zip(axes[1].patches, income_default["count"]):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 str(int(val)), ha="center", fontsize=9)
plt.tight_layout()
save_fig(fig, "chart2_default_rate_income_tier")

# --- Plotly ---
fig_px = px.bar(
    income_default, x="income_tier", y="default_rate",
    title="Default Rate by Income Tier",
    labels={"income_tier": "Income Tier", "default_rate": "Default Rate (%)"},
    color="default_rate", color_continuous_scale=["#2ecc71", "#e74c3c"],
    template="plotly_white"
)
save_fig(fig_px, "chart2_default_rate_income_tier_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# CHART 3 — Loan Amount Distribution
# ─────────────────────────────────────────────────────────────────
print("\n[3] Loan Amount Distribution")

# --- Seaborn ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for label, color in [(0, "#2ecc71"), (1, "#e74c3c")]:
    subset = df[df["defaulted"] == label]["loan_amount"]
    axes[0].hist(subset, bins=30, alpha=0.6,
                 label=f"{'Default' if label else 'No Default'}",
                 color=color)
axes[0].set_title("Loan Amount Distribution by Default Status",
                  fontsize=13, fontweight="bold")
axes[0].set_xlabel("Loan Amount ($)")
axes[0].set_ylabel("Count")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
axes[0].legend()

sns.boxplot(data=df, x="loan_size", y="loan_amount",
            hue="defaulted", palette={0: "#2ecc71", 1: "#e74c3c"},
            ax=axes[1], width=0.5, fliersize=3,
            order=["Small", "Medium", "Large", "Very Large"])
axes[1].set_title("Loan Amount by Size Category & Default",
                  fontsize=13, fontweight="bold")
axes[1].set_xlabel("Loan Size")
axes[1].set_ylabel("Loan Amount ($)")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
axes[1].legend(title="Defaulted", labels=["No", "Yes"])
plt.tight_layout()
save_fig(fig, "chart3_loan_amount_distribution")

# --- Plotly ---
fig_px = px.histogram(
    df, x="loan_amount", color="defaulted",
    barmode="overlay", opacity=0.6,
    title="Loan Amount Distribution by Default Status",
    labels={"loan_amount": "Loan Amount ($)", "defaulted": "Defaulted"},
    color_discrete_map={0: "#2ecc71", 1: "#e74c3c"},
    template="plotly_white"
)
save_fig(fig_px, "chart3_loan_amount_distribution_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# CHART 4 — Credit Score Distribution
# ─────────────────────────────────────────────────────────────────
print("\n[4] Credit Score Distribution")

# --- Seaborn ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for label, color in [(0, "#2ecc71"), (1, "#e74c3c")]:
    subset = df[df["defaulted"] == label]["credit_score"]
    axes[0].hist(subset, bins=30, alpha=0.6,
                 label=f"{'Default' if label else 'No Default'}",
                 color=color)
axes[0].set_title("Credit Score Distribution by Default Status",
                  fontsize=13, fontweight="bold")
axes[0].set_xlabel("Credit Score")
axes[0].set_ylabel("Count")
axes[0].legend()

credit_tier_default = (
    df.groupby("credit_tier", observed=True)["defaulted"]
    .mean().mul(100).round(2).reset_index()
)
credit_tier_default.columns = ["credit_tier", "default_rate"]
bars = axes[1].bar(credit_tier_default["credit_tier"],
                   credit_tier_default["default_rate"],
                   color=["#e74c3c","#e67e22","#f1c40f","#2ecc71","#27ae60"],
                   alpha=0.85, width=0.5)
axes[1].set_title("Default Rate by Credit Tier",
                  fontsize=13, fontweight="bold")
axes[1].set_xlabel("Credit Tier")
axes[1].set_ylabel("Default Rate (%)")
for bar, val in zip(bars, credit_tier_default["default_rate"]):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f"{val:.1f}%", ha="center", fontsize=9)
plt.tight_layout()
save_fig(fig, "chart4_credit_score_distribution")

# --- Plotly ---
fig_px = px.histogram(
    df, x="credit_score", color="defaulted",
    barmode="overlay", opacity=0.6,
    title="Credit Score Distribution by Default Status",
    labels={"credit_score": "Credit Score", "defaulted": "Defaulted"},
    color_discrete_map={0: "#2ecc71", 1: "#e74c3c"},
    template="plotly_white"
)
save_fig(fig_px, "chart4_credit_score_distribution_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# CHART 5 — Debt-to-Income Analysis
# ─────────────────────────────────────────────────────────────────
print("\n[5] Debt-to-Income Analysis")

# --- Seaborn ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.violinplot(data=df, x="defaulted", y="debt_to_income",
               palette={"0": "#2ecc71", "1": "#e74c3c"}, ax=axes[0])
axes[0].set_xticks([0, 1])
axes[0].set_xticklabels(["No Default", "Default"])
axes[0].set_title("Debt-to-Income by Default Status",
                  fontsize=13, fontweight="bold")
axes[0].set_ylabel("Debt-to-Income Ratio")

axes[1].scatter(
    df[df["defaulted"] == 0]["debt_to_income"],
    df[df["defaulted"] == 0]["credit_score"],
    alpha=0.3, s=15, color="#2ecc71", label="No Default"
)
axes[1].scatter(
    df[df["defaulted"] == 1]["debt_to_income"],
    df[df["defaulted"] == 1]["credit_score"],
    alpha=0.3, s=15, color="#e74c3c", label="Default"
)
axes[1].set_title("Debt-to-Income vs Credit Score",
                  fontsize=13, fontweight="bold")
axes[1].set_xlabel("Debt-to-Income Ratio")
axes[1].set_ylabel("Credit Score")
axes[1].legend()
plt.tight_layout()
save_fig(fig, "chart5_debt_to_income_analysis")

# --- Plotly ---
fig_px = px.scatter(
    df, x="debt_to_income", y="credit_score",
    color=df["defaulted"].map({0: "No Default", 1: "Default"}),
    opacity=0.4,
    title="Debt-to-Income vs Credit Score",
    labels={"debt_to_income": "Debt-to-Income Ratio",
            "credit_score": "Credit Score",
            "color": "Status"},
    color_discrete_map={"No Default": "#2ecc71", "Default": "#e74c3c"},
    template="plotly_white"
)
save_fig(fig_px, "chart5_debt_to_income_analysis_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# CHART 6 — Default Rate by Loan Purpose
# ─────────────────────────────────────────────────────────────────
print("\n[6] Default Rate by Loan Purpose")

purpose_default = (
    df.groupby("loan_purpose")["defaulted"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False)
    .reset_index()
)
purpose_default.columns = ["loan_purpose", "default_rate"]

# --- Seaborn ---
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#e74c3c" if r > df["defaulted"].mean() * 100
          else "#4a90d9" for r in purpose_default["default_rate"]]
bars = ax.barh(purpose_default["loan_purpose"],
               purpose_default["default_rate"],
               color=colors, alpha=0.85, height=0.5)
ax.axvline(df["defaulted"].mean() * 100, color="gray", linestyle="--",
           linewidth=1.5, label=f'Avg: {df["defaulted"].mean()*100:.1f}%')
ax.set_title("Default Rate by Loan Purpose", fontsize=15, fontweight="bold")
ax.set_xlabel("Default Rate (%)")
ax.set_ylabel("Loan Purpose")
ax.legend()
for bar, val in zip(bars, purpose_default["default_rate"]):
    ax.text(val + 0.2, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=9)
save_fig(fig, "chart6_default_rate_loan_purpose")

# --- Plotly ---
fig_px = px.bar(
    purpose_default, x="default_rate", y="loan_purpose",
    orientation="h",
    title="Default Rate by Loan Purpose",
    labels={"default_rate": "Default Rate (%)", "loan_purpose": "Loan Purpose"},
    color="default_rate", color_continuous_scale=["#2ecc71", "#e74c3c"],
    template="plotly_white"
)
fig_px.update_layout(yaxis={"categoryorder": "total ascending"})
save_fig(fig_px, "chart6_default_rate_loan_purpose_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# CHART 7 — Correlation Heatmap
# ─────────────────────────────────────────────────────────────────
print("\n[7] Correlation Heatmap")

numeric_cols = ["age", "income_annual", "credit_score", "loan_amount",
                "loan_term_months", "interest_rate", "employment_years",
                "debt_existing", "late_payments_2yr", "num_hard_inquiries",
                "debt_to_income", "defaulted"]

corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(13, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn",
            center=0, square=True, linewidths=0.5, ax=ax,
            annot_kws={"size": 9})
ax.set_title("Feature Correlation Matrix — Finance / Loan Default",
             fontsize=14, fontweight="bold", pad=20)
plt.tight_layout()
save_fig(fig, "chart7_correlation_heatmap")

# --- Plotly ---
fig_go = go.Figure(data=go.Heatmap(
    z=corr.values,
    x=corr.columns.tolist(),
    y=corr.columns.tolist(),
    colorscale="RdYlGn",
    zmid=0,
    text=corr.round(2).values,
    texttemplate="%{text}",
    textfont={"size": 9}
))
fig_go.update_layout(
    title="Feature Correlation Matrix — Finance / Loan Default",
    template="plotly_white",
    width=900, height=800
)
save_fig(fig_go, "chart7_correlation_heatmap_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# DONE
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"✓ Phase 2 complete. All charts saved → {PLOTS_DIR}")
print("=" * 60)