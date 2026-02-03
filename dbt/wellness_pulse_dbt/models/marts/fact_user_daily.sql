SELECT
    CAST(event_ts AS DATE) AS event_date,
    user_id,
    COUNT(*) AS events,
    COUNT(DISTINCT session_id) AS sessions,
    SUM(COALESCE(dwell_time_sec, 0)) AS total_dwell_time_sec,
    AVG(COALESCE(dwell_time_sec, 0)) AS avg_dwell_time_sec
FROM analytics.stg_user_events
GROUP BY 1, 2
