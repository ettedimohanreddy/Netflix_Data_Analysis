
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ==========================================
# 1. PROJECT PATHS
# ==========================================

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

# ==========================================
# 2. LOAD DATASET
# ==========================================

df = pd.read_csv(dataset_path)

print("\n========== NETFLIX BUSINESS INSIGHTS ==========")

# ==========================================
# 3. EXPLORATORY DATA ANALYSIS
# ==========================================

total_records = len(df)
total_columns = len(df.columns)

missing_values = df.isnull().sum()
duplicate_count = df.duplicated().sum()

print("\nDATASET OVERVIEW")
print("Total Records:", total_records)
print("Total Columns:", total_columns)
print("Duplicate Records:", duplicate_count)

print("\nDATA TYPES")
print(df.dtypes)

print("\nMISSING VALUES")
print(missing_values)

print("\nSTATISTICAL SUMMARY")
print(df.describe(include="all"))

# ==========================================
# 4. CONTENT TYPE ANALYSIS
# ==========================================

df["type"] = (
    df["type"]
    .astype("string")
    .str.strip()
)

type_counts = df["type"].value_counts()

movie_count = type_counts.get("Movie", 0)
tv_count = type_counts.get("TV Show", 0)

print("\nCONTENT TYPE DISTRIBUTION")
print(type_counts)

# ==========================================
# 5. COUNTRY-WISE ANALYSIS
# ==========================================

country_df = df[["country"]].copy()

country_df["country"] = (
    country_df["country"]
    .astype("string")
    .str.split(",")
)

country_df = country_df.explode("country")

country_df["country"] = (
    country_df["country"]
    .astype("string")
    .str.strip()
)

country_df = country_df[
    country_df["country"].notna()
    & (country_df["country"] != "")
    & (country_df["country"].str.lower() != "unknown")
]

country_counts = (
    country_df["country"]
    .value_counts()
    .head(10)
)

print("\nTOP 10 CONTENT-PRODUCING COUNTRIES")
print(country_counts)

# ==========================================
# 6. RELEASE YEAR ANALYSIS
# ==========================================

df["release_year"] = pd.to_numeric(
    df["release_year"],
    errors="coerce"
)

yearly_counts = (
    df.dropna(subset=["release_year"])
    .groupby("release_year")
    .size()
    .reset_index(name="Total_Releases")
    .sort_values("release_year")
)

yearly_counts["release_year"] = (
    yearly_counts["release_year"].astype(int)
)

if not yearly_counts.empty:
    peak_year = yearly_counts.loc[
        yearly_counts["Total_Releases"].idxmax()
    ]

    print("\nRELEASE YEAR ANALYSIS")
    print("Peak Release Year:", peak_year["release_year"])
    print("Content Released:", peak_year["Total_Releases"])

# ==========================================
# 7. RATING ANALYSIS
# ==========================================

df["rating"] = (
    df["rating"]
    .astype("string")
    .str.strip()
    .str.upper()
)

rating_counts = (
    df[
        df["rating"].notna()
        & (df["rating"] != "")
        & (df["rating"] != "UNKNOWN")
    ]["rating"]
    .value_counts()
)

print("\nRATING DISTRIBUTION")
print(rating_counts)

# ==========================================
# 8. GENRE ANALYSIS
# ==========================================

genre_df = df[["listed_in"]].copy()

genre_df["listed_in"] = (
    genre_df["listed_in"]
    .astype("string")
    .str.split(",")
)

genre_df = genre_df.explode("listed_in")

genre_df["listed_in"] = (
    genre_df["listed_in"]
    .astype("string")
    .str.strip()
)

genre_df = genre_df[
    genre_df["listed_in"].notna()
    & (genre_df["listed_in"] != "")
    & (genre_df["listed_in"].str.lower() != "unknown")
]

genre_counts = (
    genre_df["listed_in"]
    .value_counts()
)

print("\nTOP 10 GENRES")
print(genre_counts.head(10))

# ==========================================
# 9. RATING COMPARISON
# ==========================================

rating_comparison = pd.crosstab(
    df[
        df["rating"].notna()
        & (df["rating"] != "")
        & (df["rating"] != "UNKNOWN")
    ]["rating"],
    df["type"]
)

# ==========================================
# 10. CREATE BUSINESS DASHBOARD
# ==========================================

fig = make_subplots(
    rows=3,
    cols=2,
    subplot_titles=(
        "Movie vs TV Show Distribution",
        "Top 10 Content-Producing Countries",
        "Netflix Content by Release Year",
        "Top 10 Genres",
        "Content Rating Distribution",
        "Ratings Across Content Types"
    ),
    specs=[
        [{"type": "domain"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "xy"}]
    ]
)

# Chart 1: Content Type Distribution

fig.add_trace(
    go.Pie(
        labels=type_counts.index,
        values=type_counts.values,
        hole=0.4,
        name="Content Type"
    ),
    row=1,
    col=1
)

# Chart 2: Top Countries

fig.add_trace(
    go.Bar(
        x=country_counts.values,
        y=country_counts.index,
        orientation="h",
        name="Countries"
    ),
    row=1,
    col=2
)

# Chart 3: Release Year Trend

fig.add_trace(
    go.Scatter(
        x=yearly_counts["release_year"],
        y=yearly_counts["Total_Releases"],
        mode="lines+markers",
        name="Yearly Releases"
    ),
    row=2,
    col=1
)

# Chart 4: Top Genres

top_genres = genre_counts.head(10)

fig.add_trace(
    go.Bar(
        x=top_genres.values,
        y=top_genres.index,
        orientation="h",
        name="Genres"
    ),
    row=2,
    col=2
)

# Chart 5: Rating Distribution

fig.add_trace(
    go.Bar(
        x=rating_counts.index,
        y=rating_counts.values,
        name="Ratings"
    ),
    row=3,
    col=1
)

# Chart 6: Rating Comparison

for content_type in rating_comparison.columns:
    fig.add_trace(
        go.Bar(
            x=rating_comparison.index,
            y=rating_comparison[content_type],
            name=content_type
        ),
        row=3,
        col=2
    )

fig.update_layout(
    title_text="NETFLIX BUSINESS INSIGHTS DASHBOARD",
    height=1200,
    template="plotly_white",
    barmode="group",
    showlegend=True
)

fig.update_xaxes(title_text="Number of Titles", row=1, col=2)
fig.update_xaxes(title_text="Release Year", row=2, col=1)
fig.update_xaxes(title_text="Number of Titles", row=2, col=2)
fig.update_xaxes(title_text="Rating", row=3, col=1)
fig.update_xaxes(title_text="Rating", row=3, col=2)

fig.update_yaxes(title_text="Number of Titles", row=2, col=1)
fig.update_yaxes(title_text="Number of Titles", row=3, col=1)
fig.update_yaxes(title_text="Number of Titles", row=3, col=2)

dashboard_path = OUTPUT_DIR / "Netflix_Business_Dashboard.html"

fig.write_html(dashboard_path)

# ==========================================
# 11. GENERATE BUSINESS INSIGHTS
# ==========================================

insights = []

if movie_count > tv_count:
    insights.append(
        "Movies dominate the Netflix catalog compared "
        "with TV Shows."
    )
elif tv_count > movie_count:
    insights.append(
        "TV Shows dominate the Netflix catalog compared "
        "with Movies."
    )
else:
    insights.append(
        "Movies and TV Shows have equal representation."
    )

if not country_counts.empty:
    insights.append(
        f"{country_counts.index[0]} is the leading country "
        f"based on listed content count "
        f"({country_counts.iloc[0]} titles)."
    )

if not yearly_counts.empty:
    insights.append(
        f"{int(peak_year['release_year'])} has the highest "
        f"number of releases in the dataset "
        f"({int(peak_year['Total_Releases'])} titles)."
    )

if not genre_counts.empty:
    insights.append(
        f"{genre_counts.index[0]} is the most frequently "
        f"listed genre ({genre_counts.iloc[0]} entries)."
    )

if not rating_counts.empty:
    insights.append(
        f"{rating_counts.index[0]} is the most common "
        f"content rating ({rating_counts.iloc[0]} titles)."
    )

# ==========================================
# 12. GENERATE FINAL BUSINESS REPORT
# ==========================================

report_path = OUTPUT_DIR / "Netflix_Business_Insights_Report.txt"

with open(report_path, "w", encoding="utf-8") as file:

    file.write("NETFLIX BUSINESS INSIGHTS REPORT\n")
    file.write("=" * 55 + "\n\n")

    file.write("1. DATASET OVERVIEW\n")
    file.write("-" * 30 + "\n")
    file.write(f"Total Records: {total_records}\n")
    file.write(f"Total Columns: {total_columns}\n")
    file.write(f"Duplicate Records: {duplicate_count}\n\n")

    file.write("2. CONTENT TYPE ANALYSIS\n")
    file.write("-" * 30 + "\n")
    file.write(f"Movies: {movie_count}\n")
    file.write(f"TV Shows: {tv_count}\n\n")

    file.write("3. TOP 10 COUNTRIES\n")
    file.write("-" * 30 + "\n")
    file.write(country_counts.to_string())
    file.write("\n\n")

    file.write("4. RELEASE YEAR ANALYSIS\n")
    file.write("-" * 30 + "\n")

    if not yearly_counts.empty:
        file.write(
            f"Peak Release Year: {int(peak_year['release_year'])}\n"
        )
        file.write(
            f"Number of Releases: {int(peak_year['Total_Releases'])}\n"
        )

    file.write("\n5. CONTENT RATINGS\n")
    file.write("-" * 30 + "\n")
    file.write(rating_counts.to_string())
    file.write("\n\n")

    file.write("6. TOP 10 GENRES\n")
    file.write("-" * 30 + "\n")
    file.write(genre_counts.head(10).to_string())
    file.write("\n\n")

    file.write("7. BUSINESS INSIGHTS\n")
    file.write("-" * 30 + "\n")

    for i, insight in enumerate(insights, start=1):
        file.write(f"{i}. {insight}\n")

    file.write("\n8. MISSING VALUE ANALYSIS\n")
    file.write("-" * 30 + "\n")
    file.write(missing_values.to_string())

    file.write("\n\n9. CONCLUSION\n")
    file.write("-" * 30 + "\n")
    file.write(
        "This analysis provides an overview of Netflix content "
        "distribution, geographical availability, release trends, "
        "content ratings, and genres. The dashboard and findings "
        "can support data-driven content planning and further "
        "business analysis.\n"
    )

# ==========================================
# 13. FINAL OUTPUT
# ==========================================

print("\n========== TASK 6 COMPLETED ==========")

print("\nDashboard:")
print(dashboard_path)

print("\nBusiness Report:")
print(report_path)

print("\nBusiness Insights:")

for insight in insights:
    print("-", insight)
