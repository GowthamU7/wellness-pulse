from pathlib import Path
import duckdb

def main():
    project_root = Path(__file__).resolve().parents[1]
    db_path = project_root / "warehouse" / "wellness.duckdb"
    con = duckdb.connect(str(db_path))

    print("\nTop event types:")
    print(con.execute("""
        SELECT event_type, COUNT(*) AS cnt
        FROM raw.user_events
        GROUP BY event_type
        ORDER BY cnt DESC
        LIMIT 10;
    """).df())

    print("\nTop content categories:")
    print(con.execute("""
        SELECT category, COUNT(*) AS cnt
        FROM raw.health_content
        GROUP BY category
        ORDER BY cnt DESC
        LIMIT 10;
    """).df())

    print("\nMarketing engagement breakdown:")
    print(con.execute("""
        SELECT channel, event_type, COUNT(*) AS cnt
        FROM raw.marketing_events
        GROUP BY channel, event_type
        ORDER BY cnt DESC
        LIMIT 15;
    """).df())

    con.close()

if __name__ == "__main__":
    main()
