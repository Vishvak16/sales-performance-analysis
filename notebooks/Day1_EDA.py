import pandas as pd

#Load the dataset
df=pd.read_csv("data/raw/superstoreorders.csv")

#First check data
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())

#know the datatypes
print("\nData types:")
print(df.dtypes)

#check data quality
#Missing values
print("\nMissing values:")
print(df.isnull().sum())

#Duplicates
print("\nDuplicates Rows:", df.duplicated().sum())

#first 5rows
print("\nFirst 5 rows:")
print(df.head())

#convert order date and ship date to proper datetime
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=True)
df["ship_date"] = pd.to_datetime(df["ship_date"], format="mixed", dayfirst=True)

#Extract useful time columns
df["order_month"] = df["order_date"].dt.month_name()
df["order_year"] = df["order_date"].dt.year
df["order_day"] = df["order_date"].dt.day_name()
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days

#Fix sales column
df["sales"] = df["sales"].astype(str)
df["sales"] = df["sales"].str.replace("$", "", regex=False)
df["sales"] = df["sales"].str.replace(",", "", regex=False)
df["sales"] = df["sales"].str.strip()
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
print("Sales column type now:", df["sales"].dtype)

#basic Statistics
print("\nkey statistics:")
print(df[["sales", "profit", "discount", "quantity", "shipping_cost"]].describe())

#business questions
print("\n" + "="*50)
print("STEP 7:  BUSINESS QUESTIONS")
print("="*50)

print("\nQ1: Revenue by Category:")
q1 = df.groupby("category")["sales"].sum().round(2).sort_values(ascending=False)
print(q1)

print("\nQ2: Profit by Region:")
q2 = df.groupby("region")["profit"].sum().round(2).sort_values(ascending=False)
print(q2)

print("\nQ3: Orders by Customer Segment:")
q3 = df.groupby("segment")["order_id"].count().sort_values(ascending=False)
print(q3)

print("\nQ4: Avg Discount by Category:")
q4 = df.groupby("category")["discount"].mean().round(3)
print(q4)

print("\nQ5: High Discount Impact on Profit:")
high_discount = df[df["discount"] > 0.2]
normal        = df[df["discount"] <= 0.2]
print("Orders with discount > 20%  :", len(high_discount))
print("Orders with discount <= 20% :", len(normal))
print("Total profit - HIGH discount: $", round(high_discount["profit"].sum(), 2))
print("Total profit - NORMAL:        $", round(normal["profit"].sum(), 2))
print("Avg profit per HIGH discount order: $", round(high_discount["profit"].mean(), 2))
print("Avg profit per NORMAL order:        $", round(normal["profit"].mean(), 2))

print("\nQ6: Revenue and Profit by Year:")
q6 = df.groupby("year")[["sales","profit"]].sum().round(2)
print(q6)

print("\nQ7: Avg Profit by Shipping Mode:")
q7 = df.groupby("ship_mode")["profit"].mean().round(2).sort_values(ascending=False)
print(q7)

# ── STEP 8: SAVE CLEANED DATA ─────────────────────────
df.to_csv("data/processed/sales_cleaned.csv", index=False)
print("\n Cleaned data saved → data/processed/sales_cleaned.csv")

