DROP DATABASE IF EXISTS vehicle_rental_db;
CREATE DATABASE vehicle_rental_db;
USE vehicle_rental_db;

CREATE TABLE vehicles (
vehicle_id INT PRIMARY KEY,
vehicle_name VARCHAR(100),
vehicle_type VARCHAR(50),
daily_rate DECIMAL(10,2),
available_status VARCHAR(20)
);

INSERT INTO vehicles VALUES
(1, 'Honda City', 'Car', 2500, 'Available'),
(2, 'Toyota Innova', 'Car', 3500, 'Available'),
(3, 'Royal Enfield', 'Bike', 1200, 'Rented'),
(4, 'Activa', 'Scooter', 700, 'Available'),
(5, 'Mahindra Thar', 'SUV', 4500, 'Rented'),
(6, 'Hyundai Creta', 'SUV', 3200, 'Available'),
(7, 'KTM Duke', 'Bike', 1500, 'Available');

DELIMITER //

-- 1
CREATE PROCEDURE GetAllVehicles()
BEGIN
SELECT * FROM vehicles;
END //

-- 2
CREATE PROCEDURE GetAvailableVehicles()
BEGIN
SELECT * FROM vehicles WHERE available_status = 'Available';
END //

-- 3
CREATE PROCEDURE GetVehiclesByType(IN v_type VARCHAR(50))
BEGIN
SELECT * FROM vehicles WHERE vehicle_type = v_type;
END //

-- 4
CREATE PROCEDURE GetVehiclesByMaxRate(IN max_rate DECIMAL(10,2))
BEGIN
SELECT * FROM vehicles WHERE daily_rate <= max_rate;
END //

-- 5
CREATE PROCEDURE UpdateDailyRate(IN v_id INT, IN new_rate DECIMAL(10,2))
BEGIN
UPDATE vehicles SET daily_rate = new_rate WHERE vehicle_id = v_id;
END //

-- 6
CREATE PROCEDURE ChangeVehicleStatus(IN v_id INT, IN new_status VARCHAR(20))
BEGIN
UPDATE vehicles SET available_status = new_status WHERE vehicle_id = v_id;
END //

-- 7
CREATE PROCEDURE IncreaseDailyRate(IN percent DECIMAL(5,2))
BEGIN
UPDATE vehicles SET daily_rate = daily_rate + (daily_rate * percent / 100);
END //

-- 8
CREATE PROCEDURE DeleteVehicle(IN v_id INT)
BEGIN
DELETE FROM vehicles WHERE vehicle_id = v_id;
END //

-- 9
CREATE PROCEDURE GetVehiclesBetweenRates(IN min_rate DECIMAL(10,2), IN max_rate DECIMAL(10,2))
BEGIN
SELECT * FROM vehicles WHERE daily_rate BETWEEN min_rate AND max_rate;
END //

-- 10
CREATE PROCEDURE CountVehiclesByType(IN v_type VARCHAR(50))
BEGIN
SELECT COUNT(*) AS vehicle_count FROM vehicles WHERE vehicle_type = v_type;
END //
DELIMITER ;