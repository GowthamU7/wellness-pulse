WITH base AS (
    SELECT DISTINCT
        user_id
    FROM analytics.stg_user_events
),

activity AS (
    SELECT
        user_id,
        MIN(event_ts) AS first_seen_ts,
        MAX(event_ts) AS last_seen_ts,
        COUNT(*) AS total_events
    FROM analytics.stg_user_events
    GROUP BY 1
)

SELECT
    b.user_id,
    a.first_seen_ts,
    a.last_seen_ts,
    a.total_events,
    CASE
        WHEN a.total_events >= 50 THEN 'high'
        WHEN a.total_events >= 15 THEN 'medium'
        ELSE 'low'
    END AS engagement_bucket
FROM base b
LEFT JOIN activity a USING (user_id)
