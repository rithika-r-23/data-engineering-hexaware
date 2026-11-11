CREATE OR REFRESH STREAMING TABLE tp_bronze_entries
AS SELECT * FROM STREAM(workspace.default.tp_entries_raw);

CREATE OR REFRESH STREAMING TABLE tp_silver_entries
AS SELECT entry_id, visitor_id, attraction_id, visit_date, ticket_type,
          ticket_price, wait_minutes, ride_minutes,
          COALESCE(booking_channel, 'Unknown') AS booking_channel,
          ticket_price AS ticket_revenue
FROM STREAM(tp_bronze_entries)
WHERE status = 'Completed'
  AND wait_minutes >= 0
  AND ride_minutes > 0
  AND ticket_price > 0;

CREATE OR REFRESH MATERIALIZED VIEW tp_gold_attraction_summary
AS SELECT s.attraction_id,
          a.attraction_name,
          COUNT(*) AS completed_entries,
          SUM(s.ticket_revenue) AS total_revenue
FROM (SELECT DISTINCT entry_id, attraction_id, ticket_revenue FROM tp_silver_entries) s
LEFT JOIN workspace.default.tp_attractions a ON s.attraction_id = a.attraction_id
GROUP BY s.attraction_id, a.attraction_name;
