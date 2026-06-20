import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@genpact-postgres:5432/genpact_etl"
)


df = pd.read_csv("data/olist_customers_dataset.csv")

print(df.head())
print(f"Rows: {len(df)}")

df.to_sql(
    "raw_customers",
    engine,
    if_exists="append",
    index=False
)

print("customers loaded successfully")