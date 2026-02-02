"""
Wellness Pulse - Load raw CSV drops into DuckDB

This simulates loading raw data into a warehouse.
Later we can replace DuckDB with Postgres/Redshift/Snowflake.

Run:
  python scripts/load_to_duckdb.py
"""

from __future__ import annotations

from pathlib import Path
import duckdb


def newest_csv_in(folder: Path) -> Path:
    files = sorted(folder.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {folder}")
    return files[-1]


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    raw_root = project_root / "data" / "raw"
    user_events_dir = raw_root / "user_events"
    content_dir = raw_root / "health_content"
    marketing_dir = raw_root / "marketing_events"

    user_events_csv = newest_csv_in(user_events_dir)
    content_csv = newest_csv_in(content_dir)
    marketing_csv = newest_csv_in(marketing_dir)

    warehouse_dir = project_root / "warehouse"
    warehouse_dir.mkdir(exist_ok=True)

    db_path = warehouse_dir / "wellness.duckdb"

    con = duckdb.connect(str(db_path))

    # Create schemas
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    # Load CSV into raw tables (replace each run)
    con.execute("DROP TABLE IF EXISTS raw.user_events;")
    con.execute(f"""
        CREATE TABLE raw.user_events AS
        SELECT * FROM read_csv_auto('{user_events_csv.as_posix()}');
    """)

    con.execute("DROP TABLE IF EXISTS raw.health_content;")
    con.execute(f"""
        CREATE TABLE raw.health_content AS
        SELECT * FROM read_csv_auto('{content_csv.as_posix()}');
    """)

    con.execute("DROP TABLE IF EXISTS raw.marketing_events;")
    con.execute(f"""
        CREATE TABLE raw.marketing_events AS
        SELECT * FROM read_csv_auto('{marketing_csv.as_posix()}');
    """)

    # Quick row counts (sanity check)
    ue = con.execute("SELECT COUNT(*) FROM raw.user_events;").fetchone()[0]
    hc = con.execute("SELECT COUNT(*) FROM raw.health_content;").fetchone()[0]
    me = con.execute("SELECT COUNT(*) FROM raw.marketing_events;").fetchone()[0]

    print("✅ Loaded into DuckDB:", db_path)
    print(f" - raw.user_events: {ue} rows")
    print(f" - raw.health_content: {hc} rows")
    print(f" - raw.marketing_events: {me} rows")

    con.close()


if __name__ == "__main__":
    main()
