CREATE OR REFRESH STREAMING TABLE cap_bronze_entries
AS SELECT * FROM STREAM(workspace.default.tp_entries_raw);

CREATE OR REFRESH STREAMING TABLE cap_silver_entries (
  CONSTRAINT valid_wait EXPECT (wait_minutes >= 0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_ride EXPECT (ride_minutes > 0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_price EXPECT (ticket_price IS NOT NULL AND ticket_price > 0) ON VIOLATION DROP ROW
)
AS SELECT entry_id, visitor_id, attraction_id, visit_date, ticket_type,
          wait_minutes, ride_minutes, ticket_price,
          COALESCE(booking_channel, 'Unknown') AS booking_channel,
          ticket_price AS ticket_revenue
FROM STREAM(cap_bronze_entries)
WHERE status = 'Completed';

CREATE OR REFRESH MATERIALIZED VIEW cap_gold_attraction_summary
AS SELECT s.attraction_id,
          a.attraction_name,
          a.location.zone AS zone,
          COUNT(*) AS completed_entries,
          SUM(s.ticket_revenue) AS total_revenue,
          ROUND(AVG(s.wait_minutes), 2) AS avg_wait_minutes
FROM (SELECT DISTINCT * FROM cap_silver_entries) s
LEFT JOIN workspace.default.tp_attractions a ON s.attraction_id = a.attraction_id
GROUP BY s.attraction_id, a.attraction_name, a.location.zone;

CREATE OR REFRESH MATERIALIZED VIEW cap_gold_daily_revenue
AS SELECT visit_date,
          COUNT(*) AS completed_entries,
          SUM(ticket_revenue) AS total_revenue
FROM (SELECT DISTINCT * FROM cap_silver_entries) d
GROUP BY visit_date;

CREATE OR REFRESH MATERIALIZED VIEW cap_gold_ticket_mix
AS SELECT ticket_type,
          COUNT(*) AS completed_entries,
          SUM(ticket_revenue) AS total_revenue
FROM (SELECT DISTINCT * FROM cap_silver_entries) d
GROUP BY ticket_type;
