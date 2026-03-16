"""
Phase 2: Visualizations — Sales Data
Approach: Senior Lead / Data Scientist perspective
Dataset: sales_data_clean.csv
Charts: Matplotlib + Seaborn (static) & Plotly (interactive)
"""

import numpy as np
import pandas as pd
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
PLOTS_DIR  = BASE_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

PALETTE    = "Blues_d"
SNS_STYLE  = "whitegrid"
FIG_DPI    = 150

sns.set_theme(style=SNS_STYLE, palette=PALETTE)

# ─────────────────────────────────────────────────────────────────
# LOAD CLEAN DATA
# ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("PHASE 2 — VISUALIZATIONS")
print("=" * 60)

df = pd.read_csv(BASE_DIR / "sales_data_clean.csv", parse_dates=["order_date", "ship_date"])
df["month"]   = pd.to_datetime(df["order_date"]).dt.to_period("M")
df["quarter"] = pd.to_datetime(df["order_date"]).dt.to_period("Q")

print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} cols")

# ─────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────
def save_fig(fig, name, kind="mpl"):
    path = PLOTS_DIR / f"{name}.{'html' if kind == 'plotly' else 'png'}"
    if kind == "plotly":
        fig.write_html(str(path))
    else:
        fig.savefig(path, dpi=FIG_DPI, bbox_inches="tight")
        plt.close(fig)
    print(f"  ✓ Saved → {path.name}")

# ─────────────────────────────────────────────────────────────────
# 1. MONTHLY REVENUE TREND
# ─────────────────────────────────────────────────────────────────
print("\n[1] Monthly Revenue Trend")

monthly = (
    df.groupby("month")["revenue"]
    .sum()
    .reset_index()
)
monthly["month_str"] = monthly["month"].astype(str)

# --- Seaborn ---
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly, x="month_str", y="revenue", marker="o", linewidth=2.5, ax=ax)
ax.fill_between(monthly["month_str"], monthly["revenue"], alpha=0.15)
ax.set_title("Monthly Revenue Trend", fontsize=15, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(rotation=45, ha="right")
save_fig(fig, "chart1_monthly_revenue_trend")

# --- Plotly ---
fig_px = px.line(
    monthly, x="month_str", y="revenue",
    title="Monthly Revenue Trend",
    markers=True,
    labels={"month_str": "Month", "revenue": "Revenue ($)"},
    template="plotly_white"
)
fig_px.update_traces(line_width=2.5)
fig_px.update_layout(xaxis_tickangle=-45)
save_fig(fig_px, "chart1_monthly_revenue_trend_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# 2. TOP PRODUCTS BY REVENUE
# ─────────────────────────────────────────────────────────────────
print("\n[2] Top Products by Revenue")

top_products = (
    df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# --- Seaborn ---
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_products, x="revenue", y="product", palette="Blues_d", ax=ax)
ax.set_title("Top 10 Products by Revenue", fontsize=15, fontweight="bold")
ax.set_xlabel("Total Revenue ($)")
ax.set_ylabel("Product")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar in ax.patches:
    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height() / 2,
            f"${bar.get_width():,.0f}", va="center", fontsize=9)
save_fig(fig, "chart2_top_products_revenue")

# --- Plotly ---
fig_px = px.bar(
    top_products, x="revenue", y="product",
    orientation="h",
    title="Top 10 Products by Revenue",
    labels={"revenue": "Revenue ($)", "product": "Product"},
    color="revenue", color_continuous_scale="Blues",
    template="plotly_white"
)
fig_px.update_layout(yaxis={"categoryorder": "total ascending"})
save_fig(fig_px, "chart2_top_products_revenue_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# 3. REVENUE BY REGION
# ─────────────────────────────────────────────────────────────────
print("\n[3] Revenue by Region")

region_rev = (
    df.groupby("region")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
region_rev["rev_share_%"] = (region_rev["revenue"] / region_rev["revenue"].sum() * 100).round(2)

# --- Seaborn ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.barplot(data=region_rev, x="region", y="revenue", palette="Blues_d", ax=axes[0])
axes[0].set_title("Revenue by Region", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Region")
axes[0].set_ylabel("Revenue ($)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
axes[0].tick_params(axis="x", rotation=30)

axes[1].pie(
    region_rev["revenue"],
    labels=region_rev["region"],
    autopct="%1.1f%%",
    startangle=140,
    colors=sns.color_palette("Blues_d", len(region_rev))
)
axes[1].set_title("Revenue Share by Region", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig(fig, "chart3_revenue_by_region")

# --- Plotly ---
fig_px = px.pie(
    region_rev, values="revenue", names="region",
    title="Revenue Share by Region",
    template="plotly_white",
    color_discrete_sequence=px.colors.sequential.Blues_r
)
fig_px.update_traces(textinfo="percent+label")
save_fig(fig_px, "chart3_revenue_by_region_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# 4. SALES REP LEADERBOARD
# ─────────────────────────────────────────────────────────────────
print("\n[4] Sales Rep Leaderboard")

rep_perf = (
    df.groupby("sales_rep")["revenue"]
    .agg(total="sum", orders="count", avg_per_order="mean")
    .sort_values("total", ascending=False)
    .reset_index()
)

# --- Seaborn ---
fig, ax = plt.subplots(figsize=(10, 6))
bars = sns.barplot(data=rep_perf, x="total", y="sales_rep", palette="Blues_d", ax=ax)
ax.set_title("Sales Rep Leaderboard — Total Revenue", fontsize=15, fontweight="bold")
ax.set_xlabel("Total Revenue ($)")
ax.set_ylabel("Sales Rep")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar in ax.patches:
    ax.text(bar.get_width() + 300, bar.get_y() + bar.get_height() / 2,
            f"${bar.get_width():,.0f}", va="center", fontsize=9)
save_fig(fig, "chart4_sales_rep_leaderboard")

# --- Plotly ---
fig_px = px.bar(
    rep_perf, x="total", y="sales_rep",
    orientation="h",
    title="Sales Rep Leaderboard",
    labels={"total": "Total Revenue ($)", "sales_rep": "Sales Rep"},
    color="total", color_continuous_scale="Blues",
    hover_data={"orders": True, "avg_per_order": ":.2f"},
    template="plotly_white"
)
fig_px.update_layout(yaxis={"categoryorder": "total ascending"})
save_fig(fig_px, "chart4_sales_rep_leaderboard_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# 5. RETURN RATE BY PRODUCT
# ─────────────────────────────────────────────────────────────────
print("\n[5] Return Rate by Product")

return_rate = (
    df.groupby("product")["returned"]
    .apply(lambda x: pd.to_numeric(x, errors="coerce").mean() * 100)
    .round(2)
    .sort_values(ascending=False)
    .reset_index()
)
return_rate.columns = ["product", "return_rate_%"]

# --- Seaborn ---
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#d73027" if r > 20 else "#4575b4" for r in return_rate["return_rate_%"]]
sns.barplot(data=return_rate, x="return_rate_%", y="product", palette=colors, ax=ax)
ax.axvline(x=return_rate["return_rate_%"].mean(), color="red",
           linestyle="--", linewidth=1.5, label=f'Avg: {return_rate["return_rate_%"].mean():.1f}%')
ax.set_title("Return Rate by Product (%)", fontsize=15, fontweight="bold")
ax.set_xlabel("Return Rate (%)")
ax.set_ylabel("Product")
ax.legend()
save_fig(fig, "chart5_return_rate_by_product")

# --- Plotly ---
fig_px = px.bar(
    return_rate, x="return_rate_%", y="product",
    orientation="h",
    title="Return Rate by Product (%)",
    labels={"return_rate_%": "Return Rate (%)", "product": "Product"},
    color="return_rate_%",
    color_continuous_scale=["#4575b4", "#d73027"],
    template="plotly_white"
)
fig_px.update_layout(yaxis={"categoryorder": "total ascending"})
save_fig(fig_px, "chart5_return_rate_by_product_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# 6. CHANNEL MIX
# ─────────────────────────────────────────────────────────────────
print("\n[6] Channel Mix")

channel_rev = (
    df.groupby("channel")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# --- Seaborn ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.barplot(data=channel_rev, x="channel", y="revenue", palette="Blues_d", ax=axes[0])
axes[0].set_title("Revenue by Channel", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Channel")
axes[0].set_ylabel("Revenue ($)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

axes[1].pie(
    channel_rev["revenue"],
    labels=channel_rev["channel"],
    autopct="%1.1f%%",
    startangle=140,
    colors=sns.color_palette("Blues_d", len(channel_rev))
)
axes[1].set_title("Channel Revenue Share", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig(fig, "chart6_channel_mix")

# --- Plotly ---
fig_px = px.pie(
    channel_rev, values="revenue", names="channel",
    title="Channel Revenue Share",
    template="plotly_white",
    color_discrete_sequence=px.colors.sequential.Blues_r
)
fig_px.update_traces(textinfo="percent+label")
save_fig(fig_px, "chart6_channel_mix_interactive", kind="plotly")

# ─────────────────────────────────────────────────────────────────
# DONE
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"✓ Phase 2 complete. All charts saved → {PLOTS_DIR}")
print("=" * 60)