
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# TASK 4: TREND ANALYSIS BY RELEASE YEAR
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


# Step 2: Organize Content by Release Year
df["release_year"] = pd.to_numeric(
    df["release_year"],
    errors="coerce"
)

df = df.dropna(subset=["release_year"]).copy()

df["release_year"] = df["release_year"].astype(int)


# Step 3: Calculate Yearly Content Releases
yearly_counts = (
    df.groupby("release_year")
    .size()
    .reset_index(name="Total_Releases")
)

yearly_counts = yearly_counts.sort_values(
    by="release_year"
).reset_index(drop=True)

print("\n========== YEARLY CONTENT RELEASES ==========")
print(yearly_counts)


# Step 4: Calculate Yearly Growth and Decline
yearly_counts["Previous_Year_Releases"] = (
    yearly_counts["Total_Releases"].shift(1)
)

yearly_counts["Change_In_Releases"] = (
    yearly_counts["Total_Releases"]
    - yearly_counts["Previous_Year_Releases"]
)

yearly_counts["Growth_Percentage"] = (
    yearly_counts["Total_Releases"]
    .pct_change() * 100
)

print("\n========== YEARLY GROWTH ANALYSIS ==========")
print(yearly_counts.tail(15))


# Step 5: Export Yearly Analysis
summary_path = OUTPUT_DIR / "yearly_content_analysis.csv"

yearly_counts.to_csv(summary_path, index=False)

print("\nYearly Analysis Saved:", summary_path)


# Step 6: Create Yearly Trend Line Chart
plt.figure(figsize=(12, 6))

sns.lineplot(
    data=yearly_counts,
    x="release_year",
    y="Total_Releases",
    marker="o"
)

plt.title(
    "Netflix Content Releases by Year",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Release Year")
plt.ylabel("Number of Releases")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

plt.tight_layout()

line_chart_path = OUTPUT_DIR / "yearly_release_trend.png"

plt.savefig(
    line_chart_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# Step 7: Create Yearly Growth Percentage Chart
growth_data = yearly_counts.dropna(
    subset=["Growth_Percentage"]
).copy()

plt.figure(figsize=(12, 6))

sns.barplot(
    data=growth_data,
    x="release_year",
    y="Growth_Percentage"
)

plt.title(
    "Yearly Growth and Decline in Netflix Releases",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Release Year")
plt.ylabel("Growth Percentage (%)")
plt.xticks(rotation=90)
plt.axhline(y=0, linestyle="--")

plt.tight_layout()

growth_chart_path = OUTPUT_DIR / "yearly_growth_analysis.png"

plt.savefig(
    growth_chart_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# Step 8: Generate Business Insights
highest_year = yearly_counts.loc[
    yearly_counts["Total_Releases"].idxmax()
]

lowest_year = yearly_counts.loc[
    yearly_counts["Total_Releases"].idxmin()
]

average_releases = yearly_counts["Total_Releases"].mean()

report = f"""
NETFLIX RELEASE YEAR TREND ANALYSIS
Auspify Technologies Internship
========================================

DATASET OVERVIEW

Total Records Analyzed: {len(df)}
Years Covered: {yearly_counts["release_year"].min()}
to {yearly_counts["release_year"].max()}

YEARLY RELEASE INSIGHTS

Highest Release Year:
{int(highest_year["release_year"])}
Total Releases: {int(highest_year["Total_Releases"])}

Lowest Release Year:
{int(lowest_year["release_year"])}
Total Releases: {int(lowest_year["Total_Releases"])}

Average Yearly Releases:
{average_releases:.2f}

BUSINESS INSIGHTS

1. The year {int(highest_year["release_year"])}
   recorded the highest number of content releases.

2. The year {int(lowest_year["release_year"])}
   recorded the lowest number of content releases.

3. The average number of releases per year
   is {average_releases:.2f}.

CONCLUSION

The analysis highlights changes in Netflix
content releases over different years.

========================================
Task 4 Completed Successfully!
"""

# Step 9: Save Business Insights Report
report_path = OUTPUT_DIR / "release_year_analysis_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report)

print(report)

print("\nAll Output Files Saved In:", OUTPUT_DIR)

print("\nTASK 4 COMPLETED SUCCESSFULLY!")
