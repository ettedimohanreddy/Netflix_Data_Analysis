
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# TASK 3: COUNTRY-WISE NETFLIX CONTENT ANALYSIS
# ==========================================

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
TASK_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = TASK_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

dataset_path = (
    BASE_DIR
    / "Task_1_Data_Cleaning"
    / "output"
    / "cleaned_netflix.csv"
)

# Step 1: Load Cleaned Dataset
df = pd.read_csv(dataset_path)

print("\n========== DATASET LOADED ==========")
print("Dataset Shape:", df.shape)
print(df.head())


# Step 2: Prepare Country Data
df["country"] = (
    df["country"]
    .astype("string")
    .str.strip()
)

# Split multiple countries into separate rows
df["country"] = df["country"].str.split(",")

df = df.explode("country")

# Remove extra spaces
df["country"] = df["country"].str.strip()

# Remove missing and Unknown country values
df = df[
    df["country"].notna()
    & (df["country"] != "")
    & (df["country"].str.lower() != "unknown")
].copy()

print("\n========== COUNTRY DATA PREPARED ==========")
print("Total Country Records:", len(df))
print("Unique Countries:", df["country"].nunique())


# Step 3: Calculate Country-Wise Content Count
country_counts = (
    df.groupby("country")
    .size()
    .reset_index(name="Total_Content")
)

country_counts = country_counts.sort_values(
    by="Total_Content",
    ascending=False
)

print("\n========== TOP 10 CONTENT-PRODUCING COUNTRIES ==========")
print(country_counts.head(10))


# Step 4: Calculate Movie and TV Show Counts
country_type_counts = pd.crosstab(
    df["country"],
    df["type"]
)

# Ensure both columns exist
for content_type in ["Movie", "TV Show"]:
    if content_type not in country_type_counts.columns:
        country_type_counts[content_type] = 0

country_summary = country_type_counts[
    ["Movie", "TV Show"]
].copy()

country_summary["Total_Content"] = (
    country_summary["Movie"]
    + country_summary["TV Show"]
)

country_summary = country_summary.sort_values(
    by="Total_Content",
    ascending=False
).reset_index()

print("\n========== COUNTRY-WISE CONTENT SUMMARY ==========")
print(country_summary.head(10))


# Step 5: Export Country-Wise Summary
summary_path = OUTPUT_DIR / "country_wise_content_summary.csv"

country_summary.to_csv(summary_path, index=False)

print("\nCountry Summary Saved:", summary_path)


# Step 6: Create Top 10 Countries Bar Chart
top_10 = country_counts.head(10).sort_values(
    by="Total_Content",
    ascending=True
)

plt.figure(figsize=(11, 7))

ax = sns.barplot(
    data=top_10,
    x="Total_Content",
    y="country"
)

plt.title(
    "Top 10 Countries Producing Netflix Content",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Number of Titles")
plt.ylabel("Country")

for container in ax.containers:
    ax.bar_label(container, fmt="%d", padding=3)

plt.tight_layout()

chart_path = OUTPUT_DIR / "top_10_countries.png"

plt.savefig(
    chart_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# Step 7: Generate Business Insights
top_country = country_counts.iloc[0]["country"]
top_country_count = int(
    country_counts.iloc[0]["Total_Content"]
)

second_country = country_counts.iloc[1]["country"]
second_country_count = int(
    country_counts.iloc[1]["Total_Content"]
)

total_countries = country_counts["country"].nunique()

report = f"""
NETFLIX COUNTRY-WISE CONTENT ANALYSIS
Auspify Technologies Internship
========================================

DATASET OVERVIEW

Total Country Records: {len(df)}
Number of Unique Countries: {total_countries}

TOP CONTENT-PRODUCING COUNTRIES

1. {top_country}: {top_country_count} titles
2. {second_country}: {second_country_count} titles

TOP 10 COUNTRIES

{country_counts.head(10).to_string(index=False)}

BUSINESS INSIGHTS

1. {top_country} contributes the highest number
   of titles in the dataset.

2. {second_country} ranks second in content
   production.

3. Netflix content is distributed across
   {total_countries} different countries.

CONCLUSION

The analysis identifies the leading countries
contributing content to Netflix's catalogue.

========================================
Task 3 Completed Successfully!
"""

# Step 8: Save Analysis Report
report_path = OUTPUT_DIR / "country_analysis_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report)

print(report)

print("\nAll Output Files Saved In:", OUTPUT_DIR)

print("\nTASK 3 COMPLETED SUCCESSFULLY!")
