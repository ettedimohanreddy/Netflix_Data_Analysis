
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# TASK 2: CONTENT TYPE ANALYSIS DASHBOARD
# ==========================================

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
TASK_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = TASK_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Step 1: Load Cleaned Dataset from Task 1
dataset_path = (
    BASE_DIR
    / "Task_1_Data_Cleaning"
    / "output"
    / "cleaned_netflix.csv"
)

df = pd.read_csv(dataset_path)

print("\n========== DATASET LOADED ==========")
print("Dataset Shape:", df.shape)
print(df.head())


# Step 2: Standardize Content Type Labels
df["type"] = df["type"].astype("string").str.strip().str.lower()

df["type"] = df["type"].replace({
    "movie": "Movie",
    "tv show": "TV Show",
    "tv shows": "TV Show"
})


# Step 3: Count Movies and TV Shows
content_counts = df["type"].value_counts().reindex(
    ["Movie", "TV Show"],
    fill_value=0
)

total_content = int(content_counts.sum())

print("\n========== CONTENT TYPE DISTRIBUTION ==========")
print(content_counts)

print("\nTotal Netflix Content:", total_content)

if total_content == 0:
    raise ValueError("No Movie or TV Show records found!")


# Step 4: Calculate Percentages
content_percentages = (
    content_counts / total_content
) * 100

print("\n========== CONTENT PERCENTAGES ==========")
print(content_percentages.round(2))


# Step 5: Save Content Summary
content_summary = pd.DataFrame({
    "Content_Type": content_counts.index,
    "Total_Count": content_counts.values,
    "Percentage": content_percentages.values
})

summary_path = OUTPUT_DIR / "content_analysis_summary.csv"

content_summary.to_csv(summary_path, index=False)


# Step 6: Create Bar Chart
plt.figure(figsize=(9, 6))

ax = sns.barplot(
    x=content_counts.index,
    y=content_counts.values
)

plt.title(
    "Netflix Content Distribution: Movies vs TV Shows",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Content Type")
plt.ylabel("Number of Titles")

for i, value in enumerate(content_counts.values):
    ax.text(
        i,
        value + max(total_content * 0.01, 10),
        f"{value:,}",
        ha="center",
        fontsize=11
    )

plt.tight_layout()

bar_chart_path = OUTPUT_DIR / "content_distribution.png"

plt.savefig(
    bar_chart_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# Step 7: Create Pie Chart
plt.figure(figsize=(8, 8))

largest_index = content_counts.values.argmax()

explode = [
    0.05 if i == largest_index else 0
    for i in range(len(content_counts))
]

plt.pie(
    content_counts.values,
    labels=content_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    explode=explode,
    shadow=True
)

plt.title(
    "Netflix Content Type Percentage Distribution",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()

pie_chart_path = OUTPUT_DIR / "content_type_pie_chart.png"

plt.savefig(
    pie_chart_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# Step 8: Generate Business Insights
movie_count = int(content_counts["Movie"])
tv_count = int(content_counts["TV Show"])

movie_percentage = float(content_percentages["Movie"])
tv_percentage = float(content_percentages["TV Show"])

largest_category = content_counts.idxmax()
smallest_category = content_counts.idxmin()

report = f"""
NETFLIX CONTENT TYPE ANALYSIS
Auspify Technologies Internship
================================

DATASET OVERVIEW
Total Content: {total_content}

CONTENT DISTRIBUTION
Movies: {movie_count}
TV Shows: {tv_count}

PERCENTAGE DISTRIBUTION
Movies: {movie_percentage:.2f}%
TV Shows: {tv_percentage:.2f}%

BUSINESS INSIGHTS

1. Movies account for {movie_percentage:.2f}% of the dataset.

2. TV Shows account for {tv_percentage:.2f}% of the dataset.

3. {largest_category} is the larger content category.

4. {smallest_category} is the smaller content category.

CONCLUSION

In this dataset, {largest_category.lower()} represent
the larger share of Netflix titles.

================================
Task 2 Completed Successfully!
"""


# Step 9: Save Analysis Report
report_path = OUTPUT_DIR / "task2_analysis_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report)

print(report)

print("\nTask 2 Output Files Saved In:", OUTPUT_DIR)

print("\nTASK 2 COMPLETED SUCCESSFULLY!")
