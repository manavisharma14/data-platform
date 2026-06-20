import pandas as pd
from sqlalchemy import create_engine
import sys

engine = create_engine(
    "postgresql://postgres:postgres@genpact-postgres:5432/genpact_etl"
)

csv_file = sys.argv[1]
table_name = sys.argv[2]

df = pd.read_csv(csv_file)

if table_name == "raw_products":
    df = df.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length"
        }
    )

print(f"Loading {len(df):,} rows into {table_name}")

df.to_sql(
    table_name,
    engine,
    if_exists="append",
    index=False
)

print("Load completed")