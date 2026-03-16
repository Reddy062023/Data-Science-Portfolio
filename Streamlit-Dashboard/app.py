"""
Streamlit Dashboard — Data Science Portfolio
Author: Japendra
Projects: Sales EDA, Healthcare Analytics, Finance ML
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Japendra — Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent

# ─────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    sales    = pd.read_csv(ROOT_DIR / "Sales-EDA"               / "sales_data_clean.csv")
    health   = pd.read_csv(ROOT_DIR / "Healthcare-Visualization" / "healthcare_data_clean.csv")
    finance  = pd.read_csv(ROOT_DIR / "Finance-ML"              / "finance_data_clean.csv")
    finance["defaulted"] = finance["defaulted"].astype(int)
    sales["order_date"]  = pd.to_datetime(sales["order_date"])
    return sales, health, finance

sales, health, finance = load_data()

# ─────────────────────────────────────────────────────────────────
# TRAIN MODEL (cached)
# ─────────────────────────────────────────────────────────────────
@st.cache_resource
def train_model():
    df = finance.copy()
    for col in ["employment_status","loan_purpose","home_ownership","loan_grade","gender"]:
        if col in df.columns:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))
    features = ["age","income_annual","credit_score","loan_amount","loan_term_months",
                "employment_years","late_payments_2yr","interest_rate",
                "employment_status","loan_purpose","loan_grade"]
    X = df[features]
    y = df["defaulted"]
    model = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42,
                                       class_weight="balanced"))
    ])
    model.fit(X, y)
    return model, features

model, model_features = train_model()

# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/data-configuration.png", width=80)
st.sidebar.title("📊 Portfolio Dashboard")
st.sidebar.markdown("**Japendra**")
st.sidebar.markdown("Data Scientist | Python | ML")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📊 Sales Analytics", "🏥 Healthcare Analytics", "💰 Finance ML"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Datasets**")
st.sidebar.markdown(f"🛒 Sales: {len(sales):,} rows")
st.sidebar.markdown(f"🏥 Healthcare: {len(health):,} rows")
st.sidebar.markdown(f"💰 Finance: {len(finance):,} rows")

# ─────────────────────────────────────────────────────────────────
# PAGE 1 — HOME
# ─────────────────────────────────────────────────────────────────
if page == "🏠 Home":
    st.title("📊 Data Science Portfolio — Japendra")
    st.markdown("### End-to-end data analysis, visualization and machine learning projects")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Projects", "3")
    col2.metric("Total Rows Analyzed", f"{len(sales)+len(health)+len(finance):,}")
    col3.metric("ML Models Built", "3")
    col4.metric("Charts Generated", "28+")

    st.markdown("---")
    st.markdown("## Projects Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Sales EDA")
        st.markdown(f"**{len(sales):,} transactions**")
        st.markdown("- Revenue trend analysis")
        st.markdown("- Product performance")
        st.markdown("- Regional breakdown")
        st.markdown("- Sales rep leaderboard")
        st.metric("Total Revenue", f"${sales['revenue'].sum():,.0f}")

    with col2:
        st.markdown("### 🏥 Healthcare Analytics")
        st.markdown(f"**{len(health):,} patients**")
        st.markdown("- Diagnosis breakdown")
        st.markdown("- Risk factor analysis")
        st.markdown("- Readmission rates")
        st.markdown("- Clinical metrics")
        st.metric("Readmission Rate",
                  f"{health['readmitted_30d'].mean()*100:.1f}%")

    with col3:
        st.markdown("### 💰 Finance ML")
        st.markdown(f"**{len(finance):,} loans**")
        st.markdown("- Loan default prediction")
        st.markdown("- Credit risk analysis")
        st.markdown("- 3 ML models compared")
        st.markdown("- Feature importance")
        st.metric("Default Rate",
                  f"{finance['defaulted'].mean()*100:.1f}%")

    st.markdown("---")
    st.markdown("## Tech Stack")
    col1, col2, col3, col4 = st.columns(4)
    col1.info("🐍 Python 3.13+")
    col2.info("🐼 Pandas & NumPy")
    col3.info("📈 Plotly & Seaborn")
    col4.info("🤖 Scikit-learn")

# ─────────────────────────────────────────────────────────────────
# PAGE 2 — SALES ANALYTICS
# ─────────────────────────────────────────────────────────────────
elif page == "📊 Sales Analytics":
    st.title("📊 Sales Analytics Dashboard")
    st.markdown("---")

    # Filters
    col1, col2, col3 = st.columns(3)
    regions   = ["All"] + sorted(sales["region"].dropna().unique().tolist())
    channels  = ["All"] + sorted(sales["channel"].dropna().unique().tolist())
    products  = ["All"] + sorted(sales["product"].dropna().unique().tolist())

    selected_region  = col1.selectbox("Filter by Region",  regions)
    selected_channel = col2.selectbox("Filter by Channel", channels)
    selected_product = col3.selectbox("Filter by Product", products)

    # Apply filters
    filtered = sales.copy()
    if selected_region  != "All": filtered = filtered[filtered["region"]  == selected_region]
    if selected_channel != "All": filtered = filtered[filtered["channel"] == selected_channel]
    if selected_product != "All": filtered = filtered[filtered["product"] == selected_product]

    # KPIs
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue",    f"${filtered['revenue'].sum():,.0f}")
    col2.metric("Total Orders",     f"{len(filtered):,}")
    col3.metric("Avg Order Value",  f"${filtered['revenue'].mean():,.0f}")
    col4.metric("Return Rate",
                f"{pd.to_numeric(filtered['returned'], errors='coerce').mean()*100:.1f}%")

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Monthly Revenue Trend")
        monthly = filtered.copy()
        monthly["month"] = monthly["order_date"].dt.to_period("M").astype(str)
        monthly_rev = monthly.groupby("month")["revenue"].sum().reset_index()
        fig = px.line(monthly_rev, x="month", y="revenue",
                      markers=True, template="plotly_white",
                      labels={"month": "Month", "revenue": "Revenue ($)"})
        fig.update_traces(line_color="#3498db", line_width=2.5)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Revenue by Region")
        region_rev = filtered.groupby("region")["revenue"].sum().reset_index()
        fig = px.pie(region_rev, values="revenue", names="region",
                     template="plotly_white",
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 Products by Revenue")
        top_products = (filtered.groupby("product")["revenue"]
                        .sum().sort_values(ascending=False)
                        .head(10).reset_index())
        fig = px.bar(top_products, x="revenue", y="product",
                     orientation="h", template="plotly_white",
                     color="revenue", color_continuous_scale="Blues",
                     labels={"revenue": "Revenue ($)", "product": "Product"})
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Revenue by Channel")
        channel_rev = filtered.groupby("channel")["revenue"].sum().reset_index()
        fig = px.bar(channel_rev, x="channel", y="revenue",
                     template="plotly_white", color="revenue",
                     color_continuous_scale="Blues",
                     labels={"channel": "Channel", "revenue": "Revenue ($)"})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Sales Rep Leaderboard")
    rep_perf = (filtered.groupby("sales_rep")["revenue"]
                .agg(total="sum", orders="count", avg_per_order="mean")
                .sort_values("total", ascending=False).reset_index())
    rep_perf["total"]         = rep_perf["total"].round(2)
    rep_perf["avg_per_order"] = rep_perf["avg_per_order"].round(2)
    st.dataframe(rep_perf, use_container_width=True)

# ─────────────────────────────────────────────────────────────────
# PAGE 3 — HEALTHCARE ANALYTICS
# ─────────────────────────────────────────────────────────────────
elif page == "🏥 Healthcare Analytics":
    st.title("🏥 Healthcare Analytics Dashboard")
    st.markdown("---")

    # Filters
    col1, col2, col3 = st.columns(3)
    genders    = ["All"] + sorted(health["gender"].dropna().unique().tolist())
    diagnoses  = ["All"] + sorted(health["diagnosis"].dropna().unique().tolist())
    insurances = ["All"] + sorted(health["insurance_type"].dropna().unique().tolist())

    selected_gender    = col1.selectbox("Filter by Gender",    genders)
    selected_diagnosis = col2.selectbox("Filter by Diagnosis", diagnoses)
    selected_insurance = col3.selectbox("Filter by Insurance", insurances)

    # Apply filters
    filtered = health.copy()
    if selected_gender    != "All": filtered = filtered[filtered["gender"]         == selected_gender]
    if selected_diagnosis != "All": filtered = filtered[filtered["diagnosis"]      == selected_diagnosis]
    if selected_insurance != "All": filtered = filtered[filtered["insurance_type"] == selected_insurance]

    # KPIs
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients",     f"{len(filtered):,}")
    col2.metric("Avg Age",            f"{filtered['age'].mean():.1f} yrs")
    col3.metric("Readmission Rate",   f"{filtered['readmitted_30d'].mean()*100:.1f}%")
    col4.metric("Avg Hospital Days",  f"{filtered['hospital_days'].mean():.1f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Diagnosis Distribution")
        diag_counts = filtered["diagnosis"].value_counts().reset_index()
        diag_counts.columns = ["diagnosis","count"]
        fig = px.pie(diag_counts, values="count", names="diagnosis",
                     color="diagnosis",
                     color_discrete_map={"Healthy": "#2ecc71",
                                         "At Risk": "#f39c12",
                                         "Critical": "#e74c3c"},
                     template="plotly_white")
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Readmission Rate by Insurance")
        readmit = (filtered.groupby("insurance_type")["readmitted_30d"]
                   .mean().mul(100).round(2).reset_index())
        readmit.columns = ["insurance_type","readmission_rate"]
        fig = px.bar(readmit, x="readmission_rate", y="insurance_type",
                     orientation="h", template="plotly_white",
                     color="readmission_rate",
                     color_continuous_scale=["#2ecc71","#e74c3c"],
                     labels={"readmission_rate": "Readmission Rate (%)",
                             "insurance_type": "Insurance Type"})
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### BMI vs Systolic BP by Diagnosis")
        fig = px.scatter(filtered, x="bmi", y="blood_pressure_systolic",
                         color="diagnosis",
                         color_discrete_map={"Healthy": "#2ecc71",
                                             "At Risk": "#f39c12",
                                             "Critical": "#e74c3c"},
                         opacity=0.5, template="plotly_white",
                         labels={"bmi": "BMI",
                                 "blood_pressure_systolic": "Systolic BP"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Hospital Days by Diagnosis")
        fig = px.box(filtered, x="diagnosis", y="hospital_days",
                     color="diagnosis",
                     color_discrete_map={"Healthy": "#2ecc71",
                                         "At Risk": "#f39c12",
                                         "Critical": "#e74c3c"},
                     template="plotly_white",
                     labels={"diagnosis": "Diagnosis",
                             "hospital_days": "Hospital Days"})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Clinical Metrics Summary")
    clinical_cols = ["age","bmi","blood_pressure_systolic",
                     "blood_pressure_diastolic","cholesterol_total","glucose_level"]
    st.dataframe(
        filtered[clinical_cols].describe().T[["mean","50%","std","min","max"]]
        .rename(columns={"50%":"median"}).round(2),
        use_container_width=True
    )

# ─────────────────────────────────────────────────────────────────
# PAGE 4 — FINANCE ML
# ─────────────────────────────────────────────────────────────────
elif page == "💰 Finance ML":
    st.title("💰 Finance ML — Loan Default Prediction")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Analytics", "🤖 Predict Default"])

    # ── Tab 1 — Analytics ────────────────────────────────────────
    with tab1:
        # Filters
        col1, col2, col3 = st.columns(3)
        grades   = ["All"] + sorted(finance["loan_grade"].dropna().unique().tolist())
        purposes = ["All"] + sorted(finance["loan_purpose"].dropna().unique().tolist())
        emp_status = ["All"] + sorted(finance["employment_status"].dropna().unique().tolist())

        selected_grade   = col1.selectbox("Filter by Loan Grade",   grades)
        selected_purpose = col2.selectbox("Filter by Loan Purpose", purposes)
        selected_emp     = col3.selectbox("Filter by Employment",   emp_status)

        filtered = finance.copy()
        if selected_grade   != "All": filtered = filtered[filtered["loan_grade"]         == selected_grade]
        if selected_purpose != "All": filtered = filtered[filtered["loan_purpose"]       == selected_purpose]
        if selected_emp     != "All": filtered = filtered[filtered["employment_status"]  == selected_emp]

        # KPIs
        st.markdown("### Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Loans",     f"{len(filtered):,}")
        col2.metric("Default Rate",    f"{filtered['defaulted'].mean()*100:.1f}%")
        col3.metric("Avg Loan Amount", f"${filtered['loan_amount'].mean():,.0f}")
        col4.metric("Avg Credit Score",f"{filtered['credit_score'].mean():.0f}")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Default Rate by Loan Grade")
            grade_default = (filtered.groupby("loan_grade")["defaulted"]
                             .mean().mul(100).round(2).reset_index())
            grade_default.columns = ["loan_grade","default_rate"]
            fig = px.bar(grade_default, x="loan_grade", y="default_rate",
                         template="plotly_white",
                         color="default_rate",
                         color_continuous_scale=["#2ecc71","#e74c3c"],
                         labels={"loan_grade": "Loan Grade",
                                 "default_rate": "Default Rate (%)"})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Credit Score Distribution")
            fig = px.histogram(filtered, x="credit_score",
                               color=filtered["defaulted"].map(
                                   {0:"No Default", 1:"Default"}),
                               barmode="overlay", opacity=0.6,
                               template="plotly_white",
                               color_discrete_map={"No Default":"#2ecc71",
                                                   "Default":"#e74c3c"},
                               labels={"credit_score":"Credit Score",
                                       "color":"Status"})
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Default Rate by Loan Purpose")
            purpose_default = (filtered.groupby("loan_purpose")["defaulted"]
                               .mean().mul(100).round(2).reset_index())
            purpose_default.columns = ["loan_purpose","default_rate"]
            fig = px.bar(purpose_default, x="default_rate", y="loan_purpose",
                         orientation="h", template="plotly_white",
                         color="default_rate",
                         color_continuous_scale=["#2ecc71","#e74c3c"],
                         labels={"default_rate":"Default Rate (%)",
                                 "loan_purpose":"Loan Purpose"})
            fig.update_layout(yaxis={"categoryorder":"total ascending"})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Debt-to-Income vs Credit Score")
            if "debt_to_income" in filtered.columns:
                fig = px.scatter(filtered, x="debt_to_income", y="credit_score",
                                 color=filtered["defaulted"].map(
                                     {0:"No Default", 1:"Default"}),
                                 opacity=0.4, template="plotly_white",
                                 color_discrete_map={"No Default":"#2ecc71",
                                                     "Default":"#e74c3c"},
                                 labels={"debt_to_income":"Debt-to-Income",
                                         "credit_score":"Credit Score",
                                         "color":"Status"})
                st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2 — Predict ──────────────────────────────────────────
    with tab2:
        st.markdown("### 🤖 Predict Loan Default for New Customer")
        st.markdown("Enter customer details below to get a default risk prediction.")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            age              = st.slider("Age", 18, 80, 35)
            income_annual    = st.number_input("Annual Income ($)",
                                               10000, 300000, 60000, step=1000)
            credit_score     = st.slider("Credit Score", 300, 850, 650)
            loan_amount      = st.number_input("Loan Amount ($)",
                                               1000, 100000, 15000, step=500)

        with col2:
            loan_term_months = st.selectbox("Loan Term (months)",
                                            [12,24,36,48,60,72], index=2)
            employment_years = st.slider("Employment Years", 0, 30, 5)
            late_payments    = st.slider("Late Payments (2yr)", 0, 10, 0)
            interest_rate    = st.slider("Interest Rate (%)", 3.0, 30.0, 12.0)

        with col3:
            employment_status = st.selectbox("Employment Status",
                                             sorted(finance["employment_status"]
                                                    .dropna().unique().tolist()))
            loan_purpose      = st.selectbox("Loan Purpose",
                                             sorted(finance["loan_purpose"]
                                                    .dropna().unique().tolist()))
            loan_grade        = st.selectbox("Loan Grade",
                                             sorted(finance["loan_grade"]
                                                    .dropna().unique().tolist()))

        st.markdown("---")

        if st.button("🔮 Predict Default Risk", type="primary"):
            # Encode categoricals same way as training
            df_temp = finance.copy()
            encoders = {}
            for col in ["employment_status","loan_purpose","loan_grade"]:
                le = LabelEncoder()
                le.fit(df_temp[col].astype(str))
                encoders[col] = le

            emp_enc   = encoders["employment_status"].transform([employment_status])[0]
            purp_enc  = encoders["loan_purpose"].transform([loan_purpose])[0]
            grade_enc = encoders["loan_grade"].transform([loan_grade])[0]

            input_data = pd.DataFrame([[
                age, income_annual, credit_score, loan_amount, loan_term_months,
                employment_years, late_payments, interest_rate,
                emp_enc, purp_enc, grade_enc
            ]], columns=model_features)

            prob       = model.predict_proba(input_data)[0][1]
            prediction = model.predict(input_data)[0]

            st.markdown("### Prediction Result")
            col1, col2, col3 = st.columns(3)

            if prediction == 1:
                col1.error(f"⚠️ HIGH RISK — Likely to Default")
            else:
                col1.success(f"✅ LOW RISK — Unlikely to Default")

            col2.metric("Default Probability", f"{prob*100:.1f}%")
            col3.metric("Confidence",
                        f"{'High' if abs(prob-0.5) > 0.3 else 'Medium' if abs(prob-0.5) > 0.15 else 'Low'}")

            # Risk gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={"text": "Default Risk %"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar":  {"color": "#e74c3c" if prob > 0.5 else "#2ecc71"},
                    "steps": [
                        {"range": [0,  30], "color": "#d5f5e3"},
                        {"range": [30, 60], "color": "#fdebd0"},
                        {"range": [60,100], "color": "#fadbd8"}
                    ],
                    "threshold": {
                        "line":  {"color": "black", "width": 4},
                        "thickness": 0.75,
                        "value": 50
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
