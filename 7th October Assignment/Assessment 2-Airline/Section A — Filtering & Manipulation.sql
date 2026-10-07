USE airline_assessment;

SELECT *
FROM flights
WHERE source_city = 'Hyderabad';

SELECT *
FROM flights
WHERE ticket_price BETWEEN 6000 AND 20000;

SELECT *
FROM flights
WHERE ticket_price > 15000;

UPDATE flights
SET ticket_price = ticket_price * 1.05
WHERE airline = 'SkyJet';

SELECT *
FROM flights
ORDER BY ticket_price DESC
LIMIT 3;
