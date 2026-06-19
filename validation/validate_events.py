import pandas as pd
from sqlalchemy import create_engine

from rules import (
    PricePositiveRule,
    UserPresentRule,
    EventTypeRule
)

from validator import Validator


engine = create_engine(
    "postgresql://postgres:postgres@localhost:5433/genpact_etl"
)

validator = Validator([
    PricePositiveRule(),
    UserPresentRule(),
    EventTypeRule()
])

query = """
SELECT *
FROM raw_events
LIMIT 100000
"""

df = pd.read_sql(query, engine)

valid_rows = []
invalid_rows = []

for _, row in df.iterrows():

    error = validator.validate(row)

    if error:

        row["validation_error"] = error
        invalid_rows.append(row)

    else:

        valid_rows.append(row)

valid_df = pd.DataFrame(valid_rows)
invalid_df = pd.DataFrame(invalid_rows)

# Write valid records

if not valid_df.empty:

    valid_df.to_sql(
        "valid_events",
        engine,
        if_exists="append",
        index=False
    )

# Write invalid records

if not invalid_df.empty:

    invalid_df.to_sql(
        "invalid_events",
        engine,
        if_exists="append",
        index=False
    )

# -------------------------
# VALIDATION METRICS
# -------------------------

rows_processed = len(valid_rows) + len(invalid_rows)

validation_rate = (
    len(valid_rows) / rows_processed * 100
    if rows_processed > 0
    else 0
)

metrics_df = pd.DataFrame([
    {
        "rows_processed": rows_processed,
        "valid_rows": len(valid_rows),
        "invalid_rows": len(invalid_rows),
        "validation_rate": round(validation_rate, 2)
    }
])

metrics_df.to_sql(
    "validation_metrics",
    engine,
    if_exists="append",
    index=False
)

print(f"Valid rows: {len(valid_rows):,}")
print(f"Invalid rows: {len(invalid_rows):,}")
print(f"Validation Rate: {validation_rate:.2f}%")
print("Validation completed")
print("Metrics recorded")