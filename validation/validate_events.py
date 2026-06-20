from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@genpact-postgres:5432/genpact_etl"
)

with engine.begin() as conn:
    conn.execute(
        """
        INSERT INTO valid_events
        SELECT *
        FROM staging_events
        WHERE
            (price >= 0 OR price IS NULL)
            AND user_id IS NOT NULL
            AND event_type IN (
                'view',
                'cart',
                'purchase',
                'remove_from_cart'
            );
        """
    )
print("Validation completed")