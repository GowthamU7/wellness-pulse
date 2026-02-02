WITH source AS (
    SELECT * FROM raw.marketing_events
),

cleaned AS (
    SELECT
        mkt_event_id,
        CAST(event_ts AS TIMESTAMP) AS event_ts,
        user_id,
        channel,
        campaign_id,
        event_type
    FROM source
)

SELECT * FROM cleaned
