"""
Phase 3: Machine Learning — Finance / Loan Default Prediction
Approach: Production-grade ML pipeline
Dataset: finance_data_clean.csv (output from Phase 1)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import (train_test_split, StratifiedKFold,
                                     cross_val_score)
from sklearn.preprocessing    import StandardScaler, LabelEncoder
from sklearn.impute            import SimpleImputer
from sklearn.pipeline          import Pipeline
from sklearn.compose           import ColumnTransformer
from sklearn.linear_model      import LogisticRegression
from sklearn.ensemble          import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics           import (classification_report, confusion_matrix,
                                       roc_auc_score, roc_curve, precision_recall_curve,
                                       average_precision_score, ConfusionMatrixDisplay)
from sklearn.inspection        import permutation_importance
from pathlib import Path

pd.set_option("display.float_format", "{:.4f}".format)

# ─────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent
PLOTS_DIR = BASE_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────
# 1. LOAD & INSPECT
# ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1 — LOAD & INSPECT")
print("=" * 60)

df = pd.read_csv(BASE_DIR / "finance_data_clean.csv")
df["defaulted"] = df["defaulted"].astype(int)

print(f"Shape: {df.shape}")
print(f"Default rate: {df['defaulted'].mean():.3f}  ({df['defaulted'].sum()} defaults)")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum()>0]}")

# ─────────────────────────────────────────────────────────────────
# 2. FEATURE ENGINEERING (domain knowledge)
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2 — FEATURE ENGINEERING")
print("=" * 60)

fe = df.copy()

# Key ratios used in real credit scoring
if "debt_to_income" not in fe.columns:
    fe["debt_to_income"] = (fe["loan_amount"] / fe["income_annual"]).round(4)
if "monthly_payment" not in fe.columns:
    fe["monthly_payment"] = (fe["loan_amount"] / fe["loan_term_months"]).round(2)
if "payment_to_income" not in fe.columns:
    fe["payment_to_income"] = (fe["monthly_payment"] / (fe["income_annual"]/12)).round(4)
if "total_debt_ratio" not in fe.columns:
    fe["total_debt_ratio"] = ((fe["loan_amount"] + fe["debt_existing"]) / fe["income_annual"]).round(4)
if "interest_cost_total" not in fe.columns:
    fe["interest_cost_total"] = (fe["loan_amount"] * fe["interest_rate"] / 100 * fe["loan_term_months"] / 12).round(2)
if "credit_util_proxy" not in fe.columns:
    fe["credit_util_proxy"] = (fe["debt_existing"] / (fe["credit_score"] * 10 + 1)).round(4)
if "risk_per_year" not in fe.columns:
    fe["risk_per_year"] = (fe["late_payments_2yr"] / 2.0).round(2)
if "credit_age_ratio" not in fe.columns:
    fe["credit_age_ratio"] = (fe["employment_years"] / (fe["age"] - 18 + 1)).round(4)

print("Engineered features:")
print(fe[["debt_to_income","payment_to_income","total_debt_ratio"]].head(8))

# ─────────────────────────────────────────────────────────────────
# 3. BUILD PREPROCESSING PIPELINE
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3 — PREPROCESSING PIPELINE")
print("=" * 60)

numeric_features = [
    "age","income_annual","credit_score","loan_amount","loan_term_months",
    "employment_years","num_credit_accounts","num_hard_inquiries",
    "late_payments_2yr","debt_existing","interest_rate",
    "debt_to_income","payment_to_income","total_debt_ratio",
    "interest_cost_total","credit_util_proxy","risk_per_year"
]

categorical_features = ["employment_status","loan_purpose","home_ownership",
                         "loan_grade","gender","state"]

# Encode categoricals
le = LabelEncoder()
for col in categorical_features:
    fe[col + "_enc"] = le.fit_transform(fe[col].astype(str))

cat_encoded  = [c + "_enc" for c in categorical_features]
all_features = numeric_features + cat_encoded

X = fe[all_features]
y = fe["defaulted"]

# Numeric pipeline: impute then scale
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler",  StandardScaler())
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, list(range(len(numeric_features)))),
    ("cat", SimpleImputer(strategy="most_frequent"),
     list(range(len(numeric_features), len(all_features))))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {X_train.shape}  Test: {X_test.shape}")
print(f"Default rate — Train: {y_train.mean():.3f}  Test: {y_test.mean():.3f}")

# ─────────────────────────────────────────────────────────────────
# 4. TRAIN & CROSS-VALIDATE MULTIPLE MODELS
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4 — MODEL TRAINING & CROSS-VALIDATION")
print("=" * 60)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "Logistic Regression": Pipeline([
        ("pre", preprocessor),
        ("clf", LogisticRegression(C=1.0, max_iter=1000, random_state=42,
                                   class_weight="balanced"))
    ]),
    "Random Forest": Pipeline([
        ("pre", preprocessor),
        ("clf", RandomForestClassifier(n_estimators=200, max_depth=8,
                                        min_samples_leaf=10, random_state=42,
                                        n_jobs=-1, class_weight="balanced"))
    ]),
    "Gradient Boosting": Pipeline([
        ("pre", preprocessor),
        ("clf", GradientBoostingClassifier(n_estimators=200, learning_rate=0.05,
                                            max_depth=4, subsample=0.8,
                                            random_state=42))
    ])
}

results = {}
print(f"\n{'Model':<25} {'AUC-CV Mean':>12} {'AUC-CV Std':>12} {'Test AUC':>10} {'AP Score':>10}")
print("─" * 75)

for name, pipeline in models.items():
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv,
                                scoring="roc_auc", n_jobs=-1)
    pipeline.fit(X_train, y_train)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    y_pred = pipeline.predict(X_test)
    auc    = roc_auc_score(y_test, y_prob)
    ap     = average_precision_score(y_test, y_prob)

    results[name] = {
        "pipeline": pipeline,
        "cv_mean":  cv_scores.mean(),
        "cv_std":   cv_scores.std(),
        "test_auc": auc,
        "ap_score": ap,
        "y_prob":   y_prob,
        "y_pred":   y_pred
    }
    print(f"{name:<25} {cv_scores.mean():>12.4f} {cv_scores.std():>12.4f} {auc:>10.4f} {ap:>10.4f}")

# ─────────────────────────────────────────────────────────────────
# 5. EVALUATE BEST MODEL
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5 — DETAILED MODEL EVALUATION")
print("=" * 60)

best_name = max(results, key=lambda k: results[k]["test_auc"])
best      = results[best_name]
print(f"Best model: {best_name}")
print(f"\nClassification Report:")
print(classification_report(y_test, best["y_pred"],
      target_names=["No Default","Default"]))

# ─────────────────────────────────────────────────────────────────
# 6. CHARTS — ROC, PR, Confusion Matrix, Feature Importance
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6 — SAVING ML EVALUATION CHARTS")
print("=" * 60)

colors = {"Logistic Regression": "#3498db",
          "Random Forest":       "#2ecc71",
          "Gradient Boosting":   "#e74c3c"}

fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle(f"ML Evaluation — Loan Default Prediction\nBest Model: {best_name}",
             fontsize=13, fontweight="bold")

# ROC curves
for name, res in results.items():
    fpr, tpr, _ = roc_curve(y_test, res["y_prob"])
    axes[0,0].plot(fpr, tpr, label=f"{name} (AUC={res['test_auc']:.3f})",
                   color=colors[name], lw=2)
axes[0,0].plot([0,1],[0,1],"k--", lw=1, label="Random (AUC=0.500)")
axes[0,0].fill_between(*roc_curve(y_test, best["y_prob"])[:2],
                        alpha=0.07, color="steelblue")
axes[0,0].set_title("ROC Curves — All Models")
axes[0,0].set_xlabel("False Positive Rate")
axes[0,0].set_ylabel("True Positive Rate")
axes[0,0].legend(fontsize=9)

# Precision-Recall
for name, res in results.items():
    prec, rec, _ = precision_recall_curve(y_test, res["y_prob"])
    axes[0,1].plot(rec, prec, label=f"{name} (AP={res['ap_score']:.3f})",
                   color=colors[name], lw=2)
baseline_ap = y_test.mean()
axes[0,1].axhline(baseline_ap, color="gray", linestyle="--",
                   label=f"Baseline (AP={baseline_ap:.3f})")
axes[0,1].set_title("Precision-Recall Curves")
axes[0,1].set_xlabel("Recall")
axes[0,1].set_ylabel("Precision")
axes[0,1].legend(fontsize=9)

# Confusion Matrix
ConfusionMatrixDisplay(
    confusion_matrix(y_test, best["y_pred"]),
    display_labels=["No Default","Default"]
).plot(ax=axes[1,0], colorbar=False, cmap="Blues")
axes[1,0].set_title(f"Confusion Matrix — {best_name}")

# Feature Importance
perm_imp = permutation_importance(best["pipeline"], X_test, y_test,
                                   n_repeats=10, random_state=42,
                                   scoring="roc_auc")
feat_imp = pd.Series(perm_imp.importances_mean, index=all_features)
feat_imp.nlargest(12).sort_values().plot(kind="barh", ax=axes[1,1],
                                          color="steelblue", alpha=0.85)
axes[1,1].set_title("Top 12 Features (Permutation Importance)")
axes[1,1].set_xlabel("Mean AUC Drop When Permuted")

plt.tight_layout()
chart_path = PLOTS_DIR / "chart8_ml_evaluation.png"
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  ✓ Saved → {chart_path.name}")

print("\n✓ Phase 3 complete. Production ML pipeline built and evaluated.")