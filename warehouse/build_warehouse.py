import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5433/genpact_etl"
)

print("Loading validated events...")

df = pd.read_sql(
    """
    SELECT *
    FROM valid_events
    """,
    engine
)

print(f"Loaded {len(df):,} validated events")

# DIM CATEGORIES

dim_categories = (
    df[
        ["category_id", "category_code"]
    ]
    .drop_duplicates()
)

dim_categories.to_sql(
    "dim_categories",
    engine,
    if_exists="append",
    index=False
)

print(
    f"Loaded {len(dim_categories):,} categories"
)

# DIM PRODUCTS

dim_products = (
    df[
        [
            "product_id",
            "brand",
            "category_id",
            "category_code"
        ]
    ]
    .drop_duplicates()
)

dim_products.to_sql(
    "dim_products",
    engine,
    if_exists="append",
    index=False
)

print(
    f"Loaded {len(dim_products):,} products"
)

# FACT EVENTS

fact_events = (
    df[
        [
            "event_id",
            "event_time",
            "event_type",
            "product_id",
            "user_id",
            "price"
        ]
    ]
)

fact_events.to_sql(
    "fact_events",
    engine,
    if_exists="append",
    index=False
)

print(
    f"Loaded {len(fact_events):,} fact events"
)

print("Warehouse build complete")