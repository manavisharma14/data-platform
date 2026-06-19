import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:postgres@localhost:5433/genpact_etl"

CHUNK_SIZE = 100_000

engine = create_engine(DB_URL)

csv_file = "data/rees46/2019-Nov.csv"

total_rows = 0

for i, chunk in enumerate(
    pd.read_csv(csv_file, chunksize=CHUNK_SIZE)
):

    # Convert timestamp column
    chunk["event_time"] = pd.to_datetime(
        chunk["event_time"],
        errors="coerce"
    )

    # Load chunk into PostgreSQL
    chunk.to_sql(
        "raw_events",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    total_rows += len(chunk)

    print(f"Loaded {total_rows:,} rows")

    # Smoke test only: stop after 3 chunks (300k rows)
    if i == 2:
        break

print("Ingestion complete")