CREATE OR REFRESH STREAMING TABLE water_bronze_readings
AS SELECT * FROM STREAM(workspace.default.water_meter_readings_source);

CREATE OR REFRESH STREAMING TABLE water_silver_readings
AS SELECT reading_id, meter_id, zone_id, reading_time, flow_lpm, pressure_bar,
          chlorine_mg_l, consumption_liters, reading_status,
          COALESCE(source_system, 'Unknown') AS source_system
FROM STREAM(water_bronze_readings)
WHERE reading_status = 'Valid'
  AND flow_lpm > 0
  AND consumption_liters > 0;

CREATE OR REFRESH MATERIALIZED VIEW water_gold_zone_summary
AS SELECT s.zone_id,
          z.zone_name,
          SUM(s.consumption_liters) AS total_consumption,
          ROUND(AVG(s.pressure_bar), 2) AS avg_pressure,
          COUNT(*) AS reading_count
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY reading_id ORDER BY reading_time DESC) AS rn
  FROM water_silver_readings
) s
LEFT JOIN workspace.default.water_zones z ON s.zone_id = z.zone_id
WHERE s.rn = 1
GROUP BY s.zone_id, z.zone_name;
