from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://postgres:postgres@genpact-postgres:5432/genpact_etl"
)

with engine.begin() as conn:

    # DIM CATEGORIES
    conn.execute(text("""
        DROP TABLE IF EXISTS dim_categories;

        CREATE TABLE dim_categories AS
        SELECT DISTINCT
            category_id,
            category_code
        FROM valid_events;
    """))

    # DIM PRODUCTS
    conn.execute(text("""
        DROP TABLE IF EXISTS dim_products;

        CREATE TABLE dim_products AS
        SELECT DISTINCT
            product_id,
            brand,
            category_id,
            category_code
        FROM valid_events;
    """))

    # FACT EVENTS
    conn.execute(text("""
        DROP TABLE IF EXISTS fact_events;

        CREATE TABLE fact_events AS
        SELECT
            event_id,
            event_time,
            event_type,
            product_id,
            user_id,
            price
        FROM valid_events;
    """))

print("Warehouse build complete")