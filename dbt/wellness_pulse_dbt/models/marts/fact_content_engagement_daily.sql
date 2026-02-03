SELECT
    CAST(e.event_ts AS DATE) AS event_date,
    e.content_id,
    COUNT(*) FILTER (WHERE e.event_type = 'view_content') AS views,
    COUNT(*) FILTER (WHERE e.event_type = 'click_recommendation') AS rec_clicks,
    AVG(COALESCE(e.dwell_time_sec, 0)) FILTER (WHERE e.event_type = 'view_content') AS avg_view_dwell_sec
FROM analytics.stg_user_events e
WHERE e.content_id IS NOT NULL
GROUP BY 1, 2
