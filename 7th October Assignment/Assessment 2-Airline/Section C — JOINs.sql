USE airline_assessment;

-- 10
SELECT p.passenger_name,f.airline,f.source_city,f.destination_city,b.status
FROM bookings b
JOIN passengers p
ON b.passenger_id = p.passenger_id
JOIN flights f
ON b.flight_id = f.flight_id;

-- Q11
SELECT p.passenger_id,p.passenger_name,p.city,p.email,b.booking_id,b.flight_id,b.booking_date,b.seats,b.status
FROM passengers p
LEFT JOIN bookings b
ON p.passenger_id = b.passenger_id;

-- 12

SELECT b.booking_id,b.passenger_id,b.flight_id,b.booking_date,b.seats,b.status
FROM bookings b
LEFT JOIN passengers p
ON b.passenger_id = p.passenger_id
LEFT JOIN flights f
ON b.flight_id = f.flight_id
WHERE p.passenger_id IS NULL
OR f.flight_id IS NULL;