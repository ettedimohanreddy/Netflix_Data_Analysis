
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

# ==========================================
# TASK 5: CONTENT RATING & GENRE ANALYSIS
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

# Step 1: Load Dataset
df = pd.read_csv(dataset_path)

print("\n========== DATASET LOADED ==========")
print("Dataset Shape:", df.shape)
print(df.head())


# Step 2: Analyze Rating Categories
df["rating"] = (
    df["rating"]
    .astype("string")
    .str.strip()
    .str.upper()
)

rating_counts = (
    df[df["rating"].notna() & (df["rating"] != "UNKNOWN")]
    ["rating"]
    .value_counts()
    .reset_index()
)

rating_counts.columns = ["Rating", "Total_Content"]

print("\n========== RATING DISTRIBUTION ==========")
print(rating_counts)


# Step 3: Identify Most Common Genres
df["listed_in"] = (
    df["listed_in"]
    .astype("string")
    .str.strip()
)

genre_df = df[["listed_in"]].dropna().copy()

genre_df["listed_in"] = genre_df["listed_in"].str.split(",")

genre_df = genre_df.explode("listed_in")

genre_df["listed_in"] = genre_df["listed_in"].str.strip()

genre_counts = (
    genre_df["listed_in"]
    .value_counts()
    .reset_index()
)

genre_counts.columns = ["Genre", "Total_Content"]

print("\n========== TOP 10 GENRES ==========")
print(genre_counts.head(10))


# Step 4: Compare Ratings Across Content Types
rating_comparison = pd.crosstab(
    df["rating"],
    df["type"]
)

print("\n========== RATING COMPARISON ==========")
print(rating_comparison)


# Step 5: Export Analysis Results
rating_counts.to_csv(
    OUTPUT_DIR / "rating_distribution.csv",
    index=False
)

genre_counts.to_csv(
    OUTPUT_DIR / "genre_distribution.csv",
    index=False
)

rating_comparison.to_csv(
    OUTPUT_DIR / "rating_comparison.csv"
)


# Step 6: Interactive Rating Visualization
fig1 = px.bar(
    rating_counts,
    x="Rating",
    y="Total_Content",
    title="Netflix Content Distribution by Rating",
    text="Total_Content",
    labels={
        "Rating": "Content Rating",
        "Total_Content": "Number of Titles"
    }
)

fig1.update_layout(
    xaxis_title="Content Rating",
    yaxis_title="Number of Titles"
)

fig1.write_html(
    OUTPUT_DIR / "rating_distribution.html"
)

fig1.show()


# Step 7: Interactive Top 10 Genre Visualization
top_10_genres = genre_counts.head(10)

fig2 = px.bar(
    top_10_genres,
    x="Total_Content",
    y="Genre",
    orientation="h",
    title="Top 10 Netflix Genres",
    text="Total_Content",
    labels={
        "Total_Content": "Number of Titles",
        "Genre": "Content Genre"
    }
)

fig2.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

fig2.write_html(
    OUTPUT_DIR / "top_10_genres.html"
)

fig2.show()


# Step 8: Interactive Rating Comparison
rating_comparison_plot = (
    rating_comparison
    .reset_index()
    .melt(
        id_vars="rating",
        var_name="Content_Type",
        value_name="Total_Content"
    )
)

fig3 = px.bar(
    rating_comparison_plot,
    x="rating",
    y="Total_Content",
    color="Content_Type",
    barmode="group",
    title="Rating Comparison: Movies vs TV Shows",
    labels={
        "rating": "Content Rating",
        "Total_Content": "Number of Titles"
    }
)

fig3.write_html(
    OUTPUT_DIR / "rating_comparison.html"
)

fig3.show()


# Step 9: Generate Business Insights
top_rating = rating_counts.iloc[0]["Rating"]
top_rating_count = int(
    rating_counts.iloc[0]["Total_Content"]
)

top_genre = genre_counts.iloc[0]["Genre"]
top_genre_count = int(
    genre_counts.iloc[0]["Total_Content"]
)

report = f"""
NETFLIX CONTENT RATING & GENRE ANALYSIS
Auspify Technologies Internship
========================================

RATING INSIGHTS

Most Common Rating: {top_rating}
Total Content: {top_rating_count}

GENRE INSIGHTS

Most Common Genre: {top_genre}
Total Content: {top_genre_count}

TOP 10 GENRES

{genre_counts.head(10).to_string(index=False)}

RATING COMPARISON

{rating_comparison.to_string()}

BUSINESS INSIGHTS

1. {top_rating} is the most common content rating.

2. {top_genre} is the most frequently listed genre.

3. Rating distribution helps understand
   the audience classifications represented
   in Netflix's catalogue.

4. Genre distribution highlights the
   categories most represented in the dataset.

CONCLUSION

The analysis provides an overview of Netflix
content ratings, genres, and their distribution
across Movies and TV Shows.

========================================
Task 5 Completed Successfully!
"""

# Step 10: Save Business Insights Report
report_path = OUTPUT_DIR / "rating_genre_analysis_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report)

print(report)

print("\nAll Output Files Saved In:", OUTPUT_DIR)

print("\nTASK 5 COMPLETED SUCCESSFULLY!")
