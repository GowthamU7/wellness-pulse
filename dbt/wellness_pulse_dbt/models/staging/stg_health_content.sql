WITH source AS (
    SELECT * FROM raw.health_content
),

cleaned AS (
    SELECT
        content_id,
        title,
        category,
        content_type,
        difficulty,
        author,
        CAST(publish_ts AS TIMESTAMP) AS publish_ts,
        CAST(reading_time_sec AS INTEGER) AS reading_time_sec,
        tags
    FROM source
)

SELECT * FROM cleaned
