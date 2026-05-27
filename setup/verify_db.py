import sqlite3
import pandas as pd


conn = sqlite3.connect("worldbank.db")


print("\nDATABASE VERIFICATION\n")


total_rows = pd.read_sql_query(
    "SELECT COUNT(*) as count FROM indicators",
    conn
)

print(f"Total rows: {total_rows['count'][0]}")


country_count = pd.read_sql_query(
    "SELECT COUNT(DISTINCT country) as count FROM indicators",
    conn
)

print(f"Distinct countries: {country_count['count'][0]}")


year_range = pd.read_sql_query(
    "SELECT MIN(date) as min_year, MAX(date) as max_year FROM indicators",
    conn
)

print(
    f"Year range: "
    f"{year_range['min_year'][0]} "
    f"to "
    f"{year_range['max_year'][0]}"
)


metadata_rows = pd.read_sql_query(
    "SELECT COUNT(*) as count FROM country_metadata",
    conn
)

print(f"Metadata rows: {metadata_rows['count'][0]}")


df = pd.read_sql_query(
    "SELECT * FROM indicators",
    conn
)


print("\nNULL VALUE CHECK\n")


columns = [
    column
    for column in df.columns
    if column not in ["country", "date"]
]


good_columns = 0


for column in columns:

    null_percentage = (
        df[column]
        .isnull()
        .mean()
        * 100
    )

    print(
        f"{column}: "
        f"{null_percentage:.2f}% null"
    )

    if null_percentage < 50:
        good_columns += 1


print(
    f"\nIndicators with <50% null values: "
    f"{good_columns}"
)


print("\nREQUIREMENT CHECKS\n")


print(
    "Rows >= 5000:",
    total_rows["count"][0] >= 5000
)

print(
    "Countries >= 180:",
    country_count["count"][0] >= 180
)

print(
    "Metadata rows >= 180:",
    metadata_rows["count"][0] >= 180
)

print(
    "Good indicators >= 7:",
    good_columns >= 7
)


conn.close()


print("\nVerification completed successfully!")