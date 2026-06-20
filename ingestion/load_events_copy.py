import psycopg2

conn = psycopg2.connect(
    host="genpact-postgres",
    database="genpact_etl",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

csv_file = "/project/data/rees46/2019-Nov.csv"

with open(csv_file, "r") as f:
    cur.copy_expert(
        """
        COPY staging_events (
            event_time,
            event_type,
            product_id,
            category_id,
            category_code,
            brand,
            price,
            user_id,
            user_session
        )
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE
        )
        """,
        f
    )
conn.commit()
cur.close()
conn.close()

print("COPY COMPLETED")