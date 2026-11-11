CREATE OR REFRESH STREAMING TABLE wcap_bronze_readings
AS SELECT * FROM STREAM(workspace.default.water_meter_readings_source);

CREATE OR REFRESH STREAMING TABLE wcap_silver_readings (
  CONSTRAINT valid_flow EXPECT (flow_lpm > 0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_consumption EXPECT (consumption_liters > 0) ON VIOLATION DROP ROW
)
AS SELECT reading_id, meter_id, zone_id, reading_time, flow_lpm, pressure_bar,
          chlorine_mg_l, consumption_liters,
          COALESCE(source_system, 'Unknown') AS source_system,
          CASE WHEN pressure_bar < 2.5 THEN true ELSE false END AS low_pressure_flag,
          CASE WHEN chlorine_mg_l < 0.3 OR chlorine_mg_l > 1.5 THEN true ELSE false END AS quality_flag
FROM STREAM(wcap_bronze_readings)
WHERE reading_status = 'Valid';

CREATE OR REFRESH MATERIALIZED VIEW wcap_gold_clean_readings
AS SELECT r.reading_id, r.meter_id, r.zone_id, z.zone_name, z.district, z.zone_type,
          r.reading_time, CAST(r.reading_time AS DATE) AS reading_date,
          r.flow_lpm, r.pressure_bar, r.chlorine_mg_l, r.consumption_liters,
          r.low_pressure_flag, r.quality_flag
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY reading_id ORDER BY reading_time DESC) AS rn
  FROM wcap_silver_readings
) r
JOIN workspace.default.water_zones z ON r.zone_id = z.zone_id
WHERE r.rn = 1;

CREATE OR REFRESH MATERIALIZED VIEW wcap_gold_zone_summary
AS SELECT zone_id, zone_name, district,
          COUNT(*) AS reading_count,
          SUM(consumption_liters) AS total_consumption,
          ROUND(AVG(pressure_bar), 2) AS avg_pressure,
          ROUND(AVG(chlorine_mg_l), 2) AS avg_chlorine,
          SUM(CASE WHEN low_pressure_flag THEN 1 ELSE 0 END) AS low_pressure_readings,
          SUM(CASE WHEN quality_flag THEN 1 ELSE 0 END) AS quality_concerns
FROM wcap_gold_clean_readings
GROUP BY zone_id, zone_name, district;

CREATE OR REFRESH MATERIALIZED VIEW wcap_gold_district_summary
AS SELECT district,
          COUNT(*) AS reading_count,
          SUM(consumption_liters) AS total_consumption,
          ROUND(AVG(pressure_bar), 2) AS avg_pressure,
          SUM(CASE WHEN low_pressure_flag THEN 1 ELSE 0 END) AS low_pressure_readings,
          SUM(CASE WHEN quality_flag THEN 1 ELSE 0 END) AS quality_concerns
FROM wcap_gold_clean_readings
GROUP BY district;

CREATE OR REFRESH MATERIALIZED VIEW wcap_gold_daily_consumption
AS SELECT reading_date,
          COUNT(*) AS reading_count,
          SUM(consumption_liters) AS total_consumption
FROM wcap_gold_clean_readings
GROUP BY reading_date;
