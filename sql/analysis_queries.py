import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

os.makedirs("data/processed/query_results", exist_ok=True)

conn = mysql.connector.connect(
    host     = "localhost",
    user     = "root",
    password = "your_password_here",
    database = "superstore"
)
print("✅ Connected to MySQL")

def run_query(name, query):
    print("\n" + "="*60)
    print(f"QUERY: {name}")
    print("="*60)
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    filename = name.lower().replace(" ", "_") + ".csv"
    df.to_csv(f"data/processed/query_results/{filename}", index=False)
    print(f"✅ Saved → data/processed/query_results/{filename}")
    return df

# QUERY 1
q1 = """
SELECT region,
    COUNT(order_id)                          AS total_orders,
    ROUND(SUM(sales), 2)                     AS total_revenue,
    ROUND(SUM(profit), 2)                    AS total_profit,
    ROUND(AVG(profit), 2)                    AS avg_profit_per_order,
    ROUND(SUM(profit)/SUM(sales)*100, 2)     AS profit_margin_pct
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;
"""
run_query("Revenue and Profit by Region", q1)

# QUERY 2
q2 = """
SELECT year, order_month,
    COUNT(order_id)           AS total_orders,
    ROUND(SUM(sales), 2)      AS monthly_revenue,
    ROUND(SUM(profit), 2)     AS monthly_profit,
    ROUND(AVG(discount), 3)   AS avg_discount
FROM sales
GROUP BY year, order_month
ORDER BY year ASC, monthly_revenue DESC;
"""
run_query("Monthly Revenue Trend", q2)

# QUERY 3
q3 = """
SELECT category, sub_category,
    COUNT(order_id)                      AS total_orders,
    ROUND(SUM(sales), 2)                 AS total_revenue,
    ROUND(SUM(profit), 2)                AS total_profit,
    ROUND(AVG(discount)*100, 2)          AS avg_discount_pct,
    ROUND(SUM(profit)/SUM(sales)*100, 2) AS profit_margin_pct
FROM sales
GROUP BY category, sub_category
ORDER BY total_profit ASC;
"""
run_query("Product Performance by Sub Category", q3)

# QUERY 4
q4 = """
SELECT
    CASE
        WHEN discount = 0      THEN '0% No Discount'
        WHEN discount <= 0.10  THEN '1-10% Low'
        WHEN discount <= 0.20  THEN '11-20% Medium'
        WHEN discount <= 0.40  THEN '21-40% High'
        ELSE                        '40%+ Very High'
    END                            AS discount_bucket,
    COUNT(order_id)                AS total_orders,
    ROUND(SUM(sales), 2)           AS total_revenue,
    ROUND(SUM(profit), 2)          AS total_profit,
    ROUND(AVG(profit), 2)          AS avg_profit_per_order
FROM sales
GROUP BY discount_bucket
ORDER BY avg_profit_per_order DESC;
"""
run_query("Discount Impact on Profit", q4)

# QUERY 5
q5 = """
SELECT segment,
    COUNT(DISTINCT customer_name)         AS unique_customers,
    COUNT(order_id)                       AS total_orders,
    ROUND(SUM(sales), 2)                  AS total_revenue,
    ROUND(SUM(profit), 2)                 AS total_profit,
    ROUND(SUM(sales)/COUNT(DISTINCT
          customer_name), 2)              AS revenue_per_customer,
    ROUND(SUM(profit)/COUNT(order_id), 2) AS profit_per_order
FROM sales
GROUP BY segment
ORDER BY total_revenue DESC;
"""
run_query("Customer Segment Analysis", q5)

# QUERY 6
q6 = """
SELECT ship_mode,
    COUNT(order_id)               AS total_orders,
    ROUND(AVG(shipping_cost), 2)  AS avg_shipping_cost,
    ROUND(SUM(shipping_cost), 2)  AS total_shipping_cost,
    ROUND(AVG(shipping_days), 1)  AS avg_days_to_ship,
    ROUND(AVG(profit), 2)         AS avg_profit,
    ROUND(SUM(profit), 2)         AS total_profit
FROM sales
GROUP BY ship_mode
ORDER BY avg_days_to_ship ASC;
"""
run_query("Shipping Mode Analysis", q6)

# QUERY 7 - Top 10
q7 = """
SELECT product_name, category, sub_category,
    COUNT(order_id)             AS times_ordered,
    ROUND(SUM(sales), 2)        AS total_revenue,
    ROUND(SUM(profit), 2)       AS total_profit,
    ROUND(AVG(discount)*100, 2) AS avg_discount_pct
FROM sales
GROUP BY product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 10;
"""
run_query("Top 10 Most Profitable Products", q7)

# QUERY 7B - Bottom 10
q7b = """
SELECT product_name, category, sub_category,
    COUNT(order_id)             AS times_ordered,
    ROUND(SUM(sales), 2)        AS total_revenue,
    ROUND(SUM(profit), 2)       AS total_profit,
    ROUND(AVG(discount)*100, 2) AS avg_discount_pct
FROM sales
GROUP BY product_name, category, sub_category
ORDER BY total_profit ASC
LIMIT 10;
"""
run_query("Bottom 10 Loss Making Products", q7b)

# QUERY 8
q8 = """
SELECT year,
    ROUND(SUM(sales), 2)        AS yearly_revenue,
    ROUND(SUM(profit), 2)       AS yearly_profit,
    COUNT(order_id)             AS total_orders,
    ROUND(AVG(discount)*100, 2) AS avg_discount_pct,
    ROUND(SUM(profit)/SUM(sales)*100, 2) AS profit_margin_pct
FROM sales
GROUP BY year
ORDER BY year ASC;
"""
run_query("Year over Year Growth", q8)

conn.close()
print("\n✅ All queries done. Results saved in data/processed/query_results/")