WITH source AS (
    SELECT * FROM raw.user_events
),

cleaned AS (
    SELECT
        event_id,
        CAST(event_ts AS TIMESTAMP) AS event_ts,
        user_id,
        session_id,
        event_type,
        device,
        traffic_source,
        content_id,
        search_query,
        CAST(dwell_time_sec AS INTEGER) AS dwell_time_sec
    FROM source
)

SELECT * FROM cleaned
