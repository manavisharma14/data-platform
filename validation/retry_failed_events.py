import json
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5433/genpact_etl"
)

MAX_RETRIES = 3


def main():
    with engine.begin() as conn:
        failed_events = pd.read_sql(
            """
            SELECT *
            FROM invalid_events
            LIMIT 1000
            """,
            conn
        )

        if failed_events.empty:
            print("No invalid events to retry")
            return

        print(f"Found {len(failed_events):,} invalid events")

        for _, row in failed_events.iterrows():
            event_id = int(row["event_id"])
            reason = row.get("validation_error", "unknown_failure")

            existing = conn.execute(
                text("""
                    SELECT retry_count
                    FROM retry_queue
                    WHERE event_id = :event_id
                """),
                {"event_id": event_id}
            ).fetchone()

            if existing is None:
                conn.execute(
                    text("""
                        INSERT INTO retry_queue (
                            event_id,
                            failure_reason,
                            retry_count,
                            status
                        )
                        VALUES (
                            :event_id,
                            :failure_reason,
                            1,
                            'RETRYING'
                        )
                    """),
                    {
                        "event_id": event_id,
                        "failure_reason": reason
                    }
                )
            else:
                retry_count = existing[0] + 1

                if retry_count >= MAX_RETRIES:
                    raw_payload = row.dropna().to_dict()

                    conn.execute(
                        text("""
                            INSERT INTO dead_letter_queue (
                                event_id,
                                failure_reason,
                                final_retry_count,
                                raw_payload
                            )
                            VALUES (
                                :event_id,
                                :failure_reason,
                                :final_retry_count,
                                CAST(:raw_payload AS JSONB)
                            )
                        """),
                        {
                            "event_id": event_id,
                            "failure_reason": reason,
                            "final_retry_count": retry_count,
                            "raw_payload": json.dumps(raw_payload, default=str)
                        }
                    )

                    conn.execute(
                        text("""
                            UPDATE retry_queue
                            SET retry_count = :retry_count,
                                status = 'DEAD_LETTERED',
                                updated_at = NOW()
                            WHERE event_id = :event_id
                        """),
                        {
                            "retry_count": retry_count,
                            "event_id": event_id
                        }
                    )
                else:
                    conn.execute(
                        text("""
                            UPDATE retry_queue
                            SET retry_count = :retry_count,
                                status = 'RETRYING',
                                updated_at = NOW()
                            WHERE event_id = :event_id
                        """),
                        {
                            "retry_count": retry_count,
                            "event_id": event_id
                        }
                    )

        print("Retry processing completed")


if __name__ == "__main__":
    main()