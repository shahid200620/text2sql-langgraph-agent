import sqlite3
import pandas as pd
import wbdata
import requests


indicators = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "NY.GDP.PCAP.CD": "gdp_per_capita_usd",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_pct",
    "SP.POP.TOTL": "population",
    "SH.XPD.CHEX.GD.ZS": "health_expenditure_pct_gdp",
    "SP.DYN.LE00.IN": "life_expectancy",
    "EN.ATM.CO2E.PC": "co2_emissions_per_capita",
    "SL.UEM.TOTL.ZS": "unemployment_pct"
}


all_data = None

print("Fetching World Bank indicator data...")


for code, column_name in indicators.items():

    try:
        print(f"Fetching {column_name}...")

        data = wbdata.get_dataframe(
            {code: column_name},
            country="all"
        )

        data = data.reset_index()

        if all_data is None:
            all_data = data
        else:
            all_data = pd.merge(
                all_data,
                data,
                on=["country", "date"],
                how="outer"
            )

    except Exception as error:
        print(f"Skipping {column_name}")
        print(error)


all_data.columns = [
    "country",
    "date",
    *[
        column
        for column in all_data.columns
        if column not in ["country", "date"]
    ]
]


print(f"\nTotal rows fetched: {len(all_data)}")


print("\nFetching country metadata...")

url = "https://api.worldbank.org/v2/country?format=json&per_page=300"

response = requests.get(url)

countries = response.json()[1]

metadata = []

for country in countries:

    if country["region"]["id"] != "NA":

        metadata.append({
            "country_code": country["id"],
            "country_name": country["name"],
            "region": country["region"]["value"],
            "income_group": country["incomeLevel"]["value"],
            "lending_type": country["lendingType"]["value"]
        })


meta_df = pd.DataFrame(metadata)

print(f"Metadata rows fetched: {len(meta_df)}")


print("\nCreating SQLite database...")

conn = sqlite3.connect("worldbank.db")

all_data.to_sql(
    "indicators",
    conn,
    if_exists="replace",
    index=False
)

meta_df.to_sql(
    "country_metadata",
    conn,
    if_exists="replace",
    index=False
)

conn.close()


print("\nDatabase created successfully!")
print("Saved as worldbank.db")