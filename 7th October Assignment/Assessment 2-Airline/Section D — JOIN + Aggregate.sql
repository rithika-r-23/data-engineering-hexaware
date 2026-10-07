USE airline_assessment;
-- 13
SELECT p.passenger_id,p.passenger_name,
COALESCE(SUM(b.seats * f.ticket_price), 0) AS total_booking_value
FROM passengers p
LEFT JOIN bookings b
ON p.passenger_id = b.passenger_id
LEFT JOIN flights f
ON b.flight_id = f.flight_id
GROUP BY p.passenger_id, p.passenger_name;