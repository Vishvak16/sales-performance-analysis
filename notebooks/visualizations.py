import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

os.makedirs("visualizations", exist_ok=True)

# ── LOAD CLEANED DATA ────────────────────────────────────
df = pd.read_csv("data/processed/sales_cleaned.csv")

# ── STYLE SETTINGS ───────────────────────────────────────
# Set global style for all charts
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "figure.dpi"     : 150,       # high quality images
    "figure.figsize" : (10, 5),   # default chart size
    "font.size"      : 11
})

print("✅ Data loaded. Creating charts...")


# ── CHART 1: Revenue by Region ───────────────────────────
region_rev = df.groupby("region")["sales"].sum().sort_values()

fig, ax = plt.subplots(figsize=(12, 6))

colors = ["#FF6B6B" if v < 500000 else "#51CF66" for v in region_rev.values]
# Red = underperforming (below 500K), Green = performing well

bars = ax.barh(region_rev.index, region_rev.values, color=colors)

ax.set_title("Total Revenue by Region", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Revenue (USD)")
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M")
)

# Add value labels on each bar
for bar, val in zip(bars, region_rev.values):
    ax.text(
        val + 10000,
        bar.get_y() + bar.get_height()/2,
        f"${val:,.0f}",
        va="center", fontsize=8
    )

plt.tight_layout()
plt.savefig("visualizations/01_revenue_by_region.png")
plt.close()
print("✅ Chart 1 saved — Revenue by Region")


# ── CHART 2: Profit by Category ──────────────────────────
cat_profit = df.groupby("category")["profit"].sum().sort_values()

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(cat_profit.index, cat_profit.values,
              color=["#FF6B6B","#FFD43B","#51CF66"])

ax.set_title("Total Profit by Category", fontsize=16, fontweight="bold")
ax.set_ylabel("Profit (USD)")
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
)

for bar, val in zip(bars, cat_profit.values):
    ax.text(
        bar.get_x() + bar.get_width()/2,
        val + 2000,
        f"${val:,.0f}",
        ha="center", fontsize=9, fontweight="bold"
    )

plt.tight_layout()
plt.savefig("visualizations/02_profit_by_category.png")
plt.close()
print("✅ Chart 2 saved — Profit by Category")


# ── CHART 3: Discount vs Profit ──────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

scatter = ax.scatter(
    df["discount"],
    df["profit"],
    alpha=0.3,        # transparency — so overlapping dots are visible
    c=df["profit"],   # color dots by profit value
    cmap="RdYlGn",    # Red=negative, Yellow=zero, Green=positive
    s=10              # dot size
)

plt.colorbar(scatter, label="Profit")
ax.set_title("Discount vs Profit — Every Order", fontsize=16, fontweight="bold")
ax.set_xlabel("Discount Given")
ax.set_ylabel("Profit (USD)")
ax.axhline(y=0, color="black", linewidth=1.5, linestyle="--")
# axhline draws horizontal line at y=0 — the break-even line

ax.axvline(x=0.2, color="red", linewidth=1.5, linestyle="--")
# axvline draws vertical line at x=0.2 — the 20% discount danger zone

ax.text(0.21, ax.get_ylim()[1]*0.9, "20% Danger Zone →",
        color="red", fontsize=10)

plt.tight_layout()
plt.savefig("visualizations/03_discount_vs_profit.png")
plt.close()
print("✅ Chart 3 saved — Discount vs Profit Scatter")

# ── CHART 4: YoY Revenue Growth ──────────────────────────
yearly = df.groupby("year")[["sales","profit"]].sum()

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(yearly.index, yearly["sales"],
        marker="o", linewidth=2.5,
        color="#339AF0", label="Revenue")

ax.plot(yearly.index, yearly["profit"],
        marker="s", linewidth=2.5,
        color="#51CF66", label="Profit")

# Add value labels on each point
for year, rev, prof in zip(yearly.index, yearly["sales"], yearly["profit"]):
    ax.annotate(f"${rev/1e6:.1f}M",
                (year, rev),
                textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=8, color="#339AF0")
    ax.annotate(f"${prof/1e3:.0f}K",
                (year, prof),
                textcoords="offset points",
                xytext=(0, -15), ha="center", fontsize=8, color="#51CF66")

ax.set_title("Year over Year Revenue & Profit Growth",
             fontsize=16, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Amount (USD)")
ax.legend()
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M")
)

plt.tight_layout()
plt.savefig("visualizations/04_yoy_growth.png")
plt.close()
print("✅ Chart 4 saved — YoY Growth")


# ── CHART 5: Sub-Category Profit Heatmap ─────────────────
pivot = df.pivot_table(
    values  = "profit",
    index   = "region",
    columns = "category",
    aggfunc = "sum"
).round(0)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    pivot,
    annot     = True,        # show numbers inside cells
    fmt       = ",.0f",      # format as integer with commas
    cmap      = "RdYlGn",    # Red=loss, Green=profit
    linewidths= 0.5,
    ax        = ax
)
ax.set_title("Profit Heatmap: Region × Category",
             fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/05_profit_heatmap.png")
plt.close()
print("✅ Chart 5 saved — Profit Heatmap")


# ── CHART 6: Top & Bottom Products ───────────────────────
prod_profit = df.groupby("product_name")["profit"].sum()
top10       = prod_profit.nlargest(10).sort_values()
bottom10    = prod_profit.nsmallest(10).sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Top 10 — Green
axes[0].barh(
    [name[:30] for name in top10.index],  # truncate long names
    top10.values,
    color="#51CF66"
)
axes[0].set_title("✅ Top 10 Most Profitable Products",
                  fontweight="bold")
axes[0].set_xlabel("Total Profit (USD)")

# Bottom 10 — Red
axes[1].barh(
    [name[:30] for name in bottom10.index],
    bottom10.values,
    color="#FF6B6B"
)
axes[1].set_title("⚠️ Bottom 10 Loss Making Products",
                  fontweight="bold")
axes[1].set_xlabel("Total Profit (USD)")

plt.suptitle("Product Performance Comparison",
             fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("visualizations/06_top_bottom_products.png",
            bbox_inches="tight")
plt.close()
print("✅ Chart 6 saved — Top & Bottom Products")

print("\n🎉 All 6 charts saved to /visualizations/ folder!")