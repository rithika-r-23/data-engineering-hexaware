CREATE DATABASE airline_assessment;

USE airline_assessment;

CREATE TABLE flights (
    flight_id INT PRIMARY KEY,
    airline VARCHAR(50),
    source_city VARCHAR(50),
    destination_city VARCHAR(50),
	ticket_price DECIMAL(10,2)
);

INSERT INTO flights VALUES
(201, 'SkyJet', 'Hyderabad', 'Delhi', 6500),
(202, 'AirWorld', 'Mumbai', 'Bangalore', 7200),
(203, 'SkyJet', 'Delhi', 'Mumbai', 5800),
(204, 'FlyHigh', 'Hyderabad', 'Dubai', 18000),
(205, 'AirWorld', 'Bangalore', 'Delhi', 6900),
(206, 'FlyHigh', 'Mumbai', 'Singapore', 22000),
(207, 'SkyJet', 'Hyderabad', 'Mumbai', 5200);

CREATE TABLE passengers (
    passenger_id INT PRIMARY KEY,
    passenger_name VARCHAR(100),
    city VARCHAR(50),
    email VARCHAR(100)
);

INSERT INTO passengers VALUES
(1, 'Aman Verma', 'Hyderabad', ' AMAN@MAIL.COM '),
(2, 'Sara Ali', 'Mumbai', 'sara@gmail.com'),
(3, 'Rakesh Rao', 'Delhi', ''),
(4, 'Meena Shah', 'Bangalore', 'MEENA@YAHOO.COM'),
(5, 'Farah Khan', 'Hyderabad', NULL),
(6, 'John Mathew', 'Pune', 'john@gmail.com'),
(7, 'Priya Das', NULL, 'priya@mail.com');

CREATE TABLE bookings (
    booking_id INT PRIMARY KEY,
    passenger_id INT,
    flight_id INT,
    booking_date DATE,
    seats INT,
    status VARCHAR(20)
);

INSERT INTO bookings VALUES
(1001, 1, 201, '2026-06-01', 1, 'Confirmed'),
(1002, 2, 202, '2026-06-02', 2, 'Confirmed'),
(1003, 1, 204, '2026-06-03', 1, 'Confirmed'),
(1004, 3, 203, '2026-06-04', 1, 'Cancelled'),
(1005, 4, 205, '2026-06-05', 3, 'Confirmed'),
(1006, 5, 207, '2026-06-06', 2, 'Confirmed'),
(1007, 2, 206, '2026-06-07', 1, 'Confirmed'),
(1008, 20, 201, '2026-06-08', 1, 'Confirmed'),
(1009, 6, NULL, '2026-06-09', 2, 'Pending');

CREATE TABLE airline_staff (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INT,
    department VARCHAR(50),
    salary DECIMAL(10,2)
);

INSERT INTO airline_staff VALUES
(1, 'Raj Kumar', NULL, 'Management', 200000),
(2, 'Meera Rao', 1, 'Operations', 140000),
(3, 'Imran Khan', 1, 'Sales', 135000),
(4, 'Aman Shah', 2, 'Operations', 90000),
(5, 'Priya Singh', 2, 'Operations', 85000),
(6, 'Rohit Das', 3, 'Sales', 75000),
(7, 'Farah Ali', 3, 'Sales', 78000),
(8, 'Vikas Rao', 4, 'Support', 60000);