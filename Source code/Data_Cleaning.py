
import pandas as pd
from pathlib import Path

# ==========================================
# TASK 1: NETFLIX DATA CLEANING & PREPARATION
# ==========================================

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
TASK_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = TASK_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

dataset_path = BASE_DIR / "Dataset.csv"
output_path = OUTPUT_DIR / "cleaned_netflix.csv"
report_path = OUTPUT_DIR / "data_quality_report.csv"


# Step 1: Load Dataset
df = pd.read_csv(dataset_path)

print("\n========== DATASET LOADED ==========")
print("Dataset Shape:", df.shape)
print(df.head())


# Step 2: Dataset Information
print("\n========== DATASET INFORMATION ==========")
df.info()

print("\nStatistical Summary:")
print(df.describe(include="all"))

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

print("\nUnique Values:")
print(df.nunique())


# Step 3: Handle Missing Values
categorical_cols = df.select_dtypes(
    include="object"
).columns

for col in categorical_cols:
    df[col] = df[col].fillna("Unknown")

numerical_cols = df.select_dtypes(
    include="number"
).columns

for col in numerical_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].median())

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())


# Step 4: Remove Duplicate Records
duplicates_before = df.duplicated().sum()

df = df.drop_duplicates().copy()

print("\nDuplicates Before:", duplicates_before)
print("Duplicates After:", df.duplicated().sum())


# Step 5: Standardize Text Values
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Preserve correct Movie and TV Show labels
df["type"] = df["type"].str.lower().map({
    "movie": "Movie",
    "tv show": "TV Show",
    "unknown": "Unknown"
}).fillna(df["type"])

# Standardize ratings
df["rating"] = df["rating"].str.upper()


# Standardize country names
def clean_country(value):
    if value == "Unknown":
        return value

    countries = [
        country.strip().title()
        for country in value.split(",")
    ]

    return ", ".join(countries)


df["country"] = df["country"].apply(clean_country)

print("\nStandardized Content Types:")
print(df["type"].value_counts(dropna=False))

print("\nStandardized Ratings:")
print(df["rating"].unique())


# Step 6: Convert Date Column
df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

print("\nInvalid or Missing Dates:")
print(df["date_added"].isnull().sum())


# Step 7: Export Cleaned Dataset
df.to_csv(output_path, index=False)

print("\nCleaned Dataset Exported Successfully!")
print("Saved Location:", output_path)
print("Final Dataset Shape:", df.shape)


# Step 8: Generate Data Quality Report
quality_report = pd.DataFrame({
    "Column": df.columns,
    "Data_Type": df.dtypes.astype(str).values,
    "Missing_Values": df.isnull().sum().values,
    "Unique_Values": df.nunique().values
})

quality_report.to_csv(report_path, index=False)

print("\nData Quality Report:")
print(quality_report)

print("\nReport Saved:", report_path)

print("\nTASK 1 COMPLETED SUCCESSFULLY!")
