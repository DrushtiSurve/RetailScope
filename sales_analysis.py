
import pandas as pd

df = pd.read_csv("data/superstore_sales.csv")

# ==========================================
# DATA CLEANING
# ==========================================


print("Dataset dimensions:", df.shape)

print("\nColumn information:")
df.info()

#duplicate rows
duplicate_count = df.duplicated().sum()
print("\nDuplicate rows:", duplicate_count)

#date range
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=False,
    errors="coerce"
)

print("\nEarliest order date:", df["Order Date"].min())
print("Latest order date:", df["Order Date"].max())

#na dates
invalid_dates = df["Order Date"].isna().sum()
print("Invalid dates:", invalid_dates)

#sales and profit
print("\nNegative sales records:", (df["Sales"] < 0).sum())
print("Negative profit records:", (df["Profit"] < 0).sum())



#duplicate rows
print("\nDuplicate records:")
print(df[df.duplicated(keep=False)].sort_values(
    by=["Order Date", "Sales", "Profit"]
))

#overall sales and profit
print("\nTotal sales:", df["Sales"].sum())
print("Total profit:", df["Profit"].sum())

#profit distribution
print("\nProfit statistics:")
print(df["Profit"].describe())

#percentage of loss-making records
loss_count = (df["Profit"] < 0).sum()
total_records = len(df)

loss_percentage = (loss_count / total_records) * 100

print("\nLoss-making records:", loss_count)
print("Loss-making percentage:", round(loss_percentage, 2), "%")



# 9. Check missing values in each column
print("\nMissing values by column:")
print(df.isna().sum())

# 10. Check zero-value records
print("\nZero-sales records:", (df["Sales"] == 0).sum())
print("Zero-profit records:", (df["Profit"] == 0).sum())
print("Zero-quantity records:", (df["Quantity"] == 0).sum())

# 11. Check quantity and sales ranges
print("\nQuantity statistics:")
print(df["Quantity"].describe())

print("\nSales statistics:")
print(df["Sales"].describe())

# 12. Check the number of unique values
print("\nUnique regions:", df["Region"].nunique())
print("Unique states:", df["State"].nunique())
print("Unique categories:", df["Category"].nunique())
print("Unique sub-categories:", df["Sub-Category"].nunique())
print("Unique segments:", df["Segment"].nunique())



# ==========================================
# BUSINESS ANALYSIS
# ==========================================

#Sales and profit by region
region_analysis = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Orders=("Order Date", "count")
).sort_values(by="Total_Sales", ascending=False)

print("\n--- Regional Analysis ---")
print(region_analysis.round(2))


#Sales and profit by category
category_analysis = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum")
).sort_values(by="Total_Sales", ascending=False)

print("\n--- Category Analysis ---")
print(category_analysis.round(2))


#Sales and profit by sub-category
subcategory_analysis = df.groupby("Sub-Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum")
).sort_values(by="Total_Profit", ascending=True)

print("\n--- Sub-Category Analysis (Lowest Profit First) ---")
print(subcategory_analysis.round(2))


#Sales and profit by customer segment
segment_analysis = df.groupby("Segment").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum")
).sort_values(by="Total_Sales", ascending=False)

print("\n--- Customer Segment Analysis ---")
print(segment_analysis.round(2))


#Sales and profit by year
#Extract the year from Order Date
df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="mixed", errors="coerce"
)

df["Year"] = df["Order Date"].dt.year

yearly_analysis = df.groupby("Year").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum")
).sort_index()

print("\n--- Yearly Analysis ---")
print(yearly_analysis.round(2))


#five most profitable and least profitable
#sub-categories
print("\n--- Top 5 Sub-Categories by Profit ---")
print(subcategory_analysis.sort_values(
    by="Total_Profit", ascending=False
).head(5).round(2))

print("\n--- Bottom 5 Sub-Categories by Profit ---")
print(subcategory_analysis.head(5).round(2))



# ==========================================
# BUSINESS ANALYSIS PART 2
# ==========================================

#profit margin by category
category_analysis["Profit_Margin"] = (
    category_analysis["Total_Profit"] /
    category_analysis["Total_Sales"]
) * 100

print("\n--- Category Profit Margins ---")
print(category_analysis.round(2))


#profit margin by sub-category
subcategory_analysis["Profit_Margin"] = (
    subcategory_analysis["Total_Profit"] /
    subcategory_analysis["Total_Sales"]
) * 100

print("\n--- Sub-Category Profit Margins ---")
print(subcategory_analysis.sort_values(
    by="Profit_Margin", ascending=True
).round(2))


#Monthly sales and profit trends
df["Month"] = df["Order Date"].dt.month
df["Month_Name"] = df["Order Date"].dt.month_name()

monthly_analysis = df.groupby(
    ["Month", "Month_Name"]
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).sort_index(level="Month")

print("\n--- Monthly Analysis ---")
print(monthly_analysis.round(2))


#State-level performance
state_analysis = df.groupby("State").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
)

print("\n--- Top 10 States by Profit ---")
print(state_analysis.sort_values(
    by="Total_Profit", ascending=False
).head(10).round(2))

print("\n--- Bottom 10 States by Profit ---")
print(state_analysis.sort_values(
    by="Total_Profit", ascending=True
).head(10).round(2))


#Year-over-year growth
yearly_analysis["Sales_Growth_%"] = (
    yearly_analysis["Total_Sales"].pct_change() * 100
)

yearly_analysis["Profit_Growth_%"] = (
    yearly_analysis["Total_Profit"].pct_change() * 100
)

print("\n--- Year-over-Year Growth ---")
print(yearly_analysis.round(2))


#Overall profit margin
overall_profit_margin = (
    df["Profit"].sum() / df["Sales"].sum()
) * 100

print("\nOverall Profit Margin:", round(
    overall_profit_margin, 2
), "%")


# ==========================================
# FINAL PYTHON ANALYSIS
# ==========================================

#Year-wise monthly sales 
monthly_year_analysis = df.groupby(
    ["Year", "Month"]
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).reset_index()

print("\n--- Year-wise Monthly Sales ---")
print(monthly_year_analysis.round(2).to_string(index=False))


#Profit margin by region
region_analysis["Profit_Margin"] = (
    region_analysis["Total_Profit"] /
    region_analysis["Total_Sales"]
) * 100

print("\n--- Regional Profit Margins ---")
print(region_analysis.round(2))


#Profit margin by customer segment
segment_analysis["Profit_Margin"] = (
    segment_analysis["Total_Profit"] /
    segment_analysis["Total_Sales"]
) * 100

print("\n--- Segment Profit Margins ---")
print(segment_analysis.round(2))


#loss-making sub-categories
loss_analysis = df[df["Profit"] < 0].groupby(
    "Sub-Category"
).agg(
    Loss_Records=("Profit", "count"),
    Total_Loss=("Profit", "sum")
).sort_values(by="Total_Loss")

print("\n--- Loss Analysis by Sub-Category ---")
print(loss_analysis.round(2))


#loss-making regions
regional_loss = df[df["Profit"] < 0].groupby(
    "Region"
).agg(
    Loss_Records=("Profit", "count"),
    Total_Loss=("Profit", "sum")
).sort_values(by="Total_Loss")

print("\n--- Loss Analysis by Region ---")
print(regional_loss.round(2))


#largest individual loss
print("\n--- Largest Individual Loss ---")
print(df.loc[df["Profit"].idxmin()])


#largest individual profit
print("\n--- Largest Individual Profit ---")
print(df.loc[df["Profit"].idxmax()])













# ==========================================
# EXPORT ANALYSIS RESULTS
# ==========================================

import os

# Creating outputs folder if they dont exist
os.makedirs("outputs", exist_ok=True)

# Export cleaned master dataset
df.to_csv("outputs/cleaned_sales.csv", index=False)

# Export analysis tables
region_analysis.to_csv("outputs/regional_analysis.csv")
category_analysis.to_csv("outputs/category_analysis.csv")
subcategory_analysis.to_csv("outputs/subcategory_analysis.csv")
segment_analysis.to_csv("outputs/segment_analysis.csv")
yearly_analysis.to_csv("outputs/yearly_analysis.csv")
monthly_analysis.to_csv("outputs/monthly_analysis.csv")
monthly_year_analysis.to_csv("outputs/monthly_year_analysis.csv")
state_analysis.to_csv("outputs/state_analysis.csv")
loss_analysis.to_csv("outputs/loss_by_category.csv")
regional_loss.to_csv("outputs/loss_by_region.csv")

print("\n================================")
print("ALL ANALYSIS FILES EXPORTED!")
print("================================")

print("\nFiles saved in the outputs folder.")
