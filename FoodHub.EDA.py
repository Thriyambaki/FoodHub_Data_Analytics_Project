
# FOODHUB DATA ANALYTICS PROJECT
# Stage 1: Import datasets using Pandas

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


# Locate the project folder
project_folder = Path(__file__).resolve().parent
data_folder = project_folder / "data"

# Load all seven CSV files

orders = pd.read_csv(
    data_folder / "Orders_Cleaned.csv",
    encoding="utf-8-sig",
    dtype={"order_id": "string"}
)

customers = pd.read_csv(
    data_folder / "customers.csv",
    encoding="utf-8-sig",
    dtype={"customer_id": "string"}
)

restaurants = pd.read_csv(
    data_folder / "Restaurants.csv",
    encoding="utf-8-sig",
    dtype={"restaurant_id": "string"}
)

menu_items = pd.read_csv(
    data_folder / "Menu_Items.csv",
    encoding="utf-8-sig",
    dtype={"item_id": "string", "restaurant_id": "string"}
)

delivery_partners = pd.read_csv(
    data_folder / "Delivery_Partners.csv",
    encoding="utf-8-sig",
    dtype={"partner_id": "string"}
)

payments = pd.read_csv(
    data_folder / "Payments.csv",
    encoding="utf-8-sig",
    dtype={"payment_id": "string", "order_id": "string"}
)

returns = pd.read_csv(
    data_folder / "Returns_Cleaned.csv",
    encoding="utf-8-sig",
    dtype={"return_id": "string", "order_id": "string"}
)

print("All 7 FoodHub CSV files imported successfully!")




# Stage 2: Verify imported datasets

print("\nFOODHUB DATASET SUMMARY")
print("--------------------------------")

datasets = {
    "Orders": orders,
    "Customers": customers,
    "Restaurants": restaurants,
    "Menu Items": menu_items,
    "Delivery Partners": delivery_partners,
    "Payments": payments,
    "Returns": returns
}

for name, df in datasets.items():
    print(
        name, ":",
        df.shape[0], "rows,",
        df.shape[1], "columns"
    )

print("\nFIRST FIVE ORDERS")
print(orders.head())



# Check missing and duplicate Order IDs

print("\nORDERS DATA VERIFICATION")
print("-----------------------------")

print("Total Rows:", len(orders))

print("Missing Order IDs:",
      orders["order_id"].isna().sum())

print("Blank Order IDs:",
      orders["order_id"].fillna("").str.strip().eq("").sum())

print("Unique Order IDs:",
      orders["order_id"].nunique())

print("Duplicate Order IDs:",
      orders["order_id"].dropna().duplicated().sum())

print("\nOrder Status Counts:")
print(orders["order_status"].value_counts(dropna=False))




# Keep only orders with valid Order IDs

orders = orders[
    orders["order_id"].notna()
    & orders["order_id"].str.strip().ne("")
].copy()

print("Total valid orders:", len(orders))



# Standardize order status labels

orders["order_status"] = (
    orders["order_status"]
    .astype("string")
    .str.strip()
    .str.title()
)

print("\nCorrected Order Status Counts:")
print(orders["order_status"].value_counts())



print("\nFINAL ORDERS VERIFICATION")
print("-----------------------------")

print("Total Orders:", len(orders))
print("Unique Orders:", orders["order_id"].nunique())
print("Duplicate Orders:", orders["order_id"].duplicated().sum())

print("\nOrder Status:")
print(orders["order_status"].value_counts())



print("\nUNNAMED COLUMNS")

for col in orders.columns:
    if col.startswith("Unnamed:"):
        print(col, "- Non-empty values:", orders[col].notna().sum())
        print(orders[col].dropna().head())



# Remove extra unnamed Excel columns

orders = orders.loc[
    :, ~orders.columns.str.startswith("Unnamed:")
].copy()

print("\nFINAL ORDERS DATASET")
print("Rows:", orders.shape[0])
print("Columns:", orders.shape[1])

print("\nColumn Names:")
print(orders.columns.tolist())



# EDA Question 1: Total Sales Revenue

print("\nEDA QUESTION 1: TOTAL SALES")
print("--------------------------------")

# Select delivered orders
delivered_orders = orders[
    orders["order_status"] == "Delivered"
]

# Calculate sales revenue
total_sales = delivered_orders["order_amount"].sum()

print("Delivered Orders:", len(delivered_orders))
print(f"Total Sales Revenue: Rs. {total_sales:,.2f}")



# EDA QUESTION 2: CITY-WISE SALES ANALYSIS

print("\nEDA QUESTION 2: CITY-WISE SALES")
print("--------------------------------")

# Group delivered orders by city
city_sales = (
    delivered_orders.groupby("city")["order_amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nCity-wise Sales Revenue:")
print(city_sales)

# Identify the highest revenue city
print("\nHighest Sales City:", city_sales.idxmax())
print(f"Highest City Revenue: Rs. {city_sales.max():,.2f}")





# EDA QUESTION 2: CITY-WISE SALES BAR CHART

print("\nCreating City-wise Sales Chart...")

plt.figure(figsize=(10, 6))

plt.bar(
    city_sales.index,
    city_sales.values,
    color="steelblue"
)

plt.title("FoodHub - City-wise Sales Revenue")
plt.xlabel("City")
plt.ylabel("Sales Revenue (Rs.)")

plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()

# Save chart to the project folder
plt.savefig(
    project_folder / "city_wise_sales.png",
    dpi=300
)

plt.show()

print("City-wise Sales Chart saved successfully!")



# EDA QUESTION 3: MONTHLY SALES TREND

print("\nEDA QUESTION 3: MONTHLY SALES TREND")
print("-------------------------------------")

# Convert order_date to datetime
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    dayfirst=True,
    errors="coerce"
)

# Select delivered orders after date conversion
delivered_orders = orders[
    orders["order_status"] == "Delivered"
].copy()

# Create a Year-Month column
delivered_orders["year_month"] = (
    delivered_orders["order_date"].dt.to_period("M")
)

print("\nSample Dates:")
print(delivered_orders[
    ["order_date", "year_month"]
].head())





# Calculate monthly sales revenue

monthly_sales = (
    delivered_orders.groupby("year_month")["order_amount"]
    .sum()
    .sort_index()
)

print("\nMONTHLY SALES REVENUE")
print("-----------------------------")
print(monthly_sales)

print("\nHighest Sales Month:", monthly_sales.idxmax())
print(f"Highest Monthly Revenue: Rs. {monthly_sales.max():,.2f}")




# Create Monthly Sales Trend Line Chart

print("\nCreating Monthly Sales Trend Chart...")

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o",
    linestyle="-",
    linewidth=2,
    color="royalblue"
)

plt.title("FoodHub - Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales Revenue (Rs.)")

plt.xticks(rotation=45, ha="right")
plt.grid(True, linestyle="--", alpha=0.3)

plt.tight_layout()

# Save chart
plt.savefig(
    project_folder / "monthly_sales_trend.png",
    dpi=300
)

plt.show()

print("Monthly Sales Trend Chart saved successfully!")



print("\nRESTAURANTS COLUMN NAMES")
print(restaurants.columns.tolist())

print("\nFIRST FIVE RESTAURANTS")
print(restaurants.head())



# EDA QUESTION 4: RESTAURANT ANALYSIS

print("\nEDA QUESTION 4: RESTAURANT ANALYSIS")
print("-------------------------------------")

print("Delivered Orders:", len(delivered_orders))

print("Unique Restaurant IDs in Orders:",
      delivered_orders["restaurant_id"].nunique())

print("Unique Restaurant IDs in Restaurants:",
      restaurants["restaurant_id"].nunique())



# EDA QUESTION 4: TOP 10 RESTAURANTS BY SALES

print("\nEDA QUESTION 4: TOP 10 RESTAURANTS")
print("-------------------------------------")

restaurant_orders = pd.merge(
    delivered_orders,
    restaurants[["restaurant_id", "restaurant_name"]],
    on="restaurant_id",
    how="left",
    validate="many_to_one"
)

print("Delivered Orders:", len(delivered_orders))
print("Rows After Merge:", len(restaurant_orders))

print("Missing Restaurant Names:",
      restaurant_orders["restaurant_name"].isna().sum())




# EDA QUESTION 4: TOP 10 RESTAURANTS BY SALES

restaurant_sales = (
    restaurant_orders
    .groupby(["restaurant_id", "restaurant_name"])["order_amount"]
    .sum()
    .sort_values(ascending=False)
)

top_10_restaurants = restaurant_sales.head(10)

print("\nTOP 10 RESTAURANTS BY SALES")
print("--------------------------------")

print(top_10_restaurants)

print("\nHighest Sales Restaurant:",
      top_10_restaurants.index[0][1])

print(f"Highest Restaurant Revenue: Rs. {top_10_restaurants.iloc[0]:,.2f}")




# Top 10 Restaurants - Horizontal Bar Chart

# Prepare labels containing restaurant name and ID
restaurant_labels = [
    f"{name} ({rid})"
    for rid, name in top_10_restaurants.index
]

plt.figure(figsize=(11, 7))

plt.barh(
    restaurant_labels[::-1],
    top_10_restaurants.values[::-1],
    color="teal"
)

plt.title("FoodHub - Top 10 Restaurants by Sales")
plt.xlabel("Sales Revenue (Rs.)")
plt.ylabel("Restaurant")

plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()

plt.savefig(
    project_folder / "top_10_restaurants.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Top 10 Restaurants Chart saved successfully!")





