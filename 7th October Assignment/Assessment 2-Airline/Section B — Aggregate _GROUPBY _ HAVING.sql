USE airline_assessment;
-- 6
SELECT airline,
AVG(ticket_price) AS average_ticket_price
FROM flights
GROUP BY airline;



-- 7
SELECT flight_id,
SUM(seats) AS total_seats_booked
FROM bookings
GROUP BY flight_id;

-- Q8
SELECT airline,
AVG(ticket_price) AS average_ticket_price
FROM flights
GROUP BY airline
HAVING AVG(ticket_price) > 8000;

-- 9


SELECT f.airline,
SUM(b.seats * f.ticket_price) AS total_booking_value
FROM bookings b
JOIN flights f
ON b.flight_id = f.flight_id
GROUP BY f.airline;