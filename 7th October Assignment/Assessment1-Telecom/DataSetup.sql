CREATE DATABASE telecom_assessment;

USE telecom_assessment;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    mobile VARCHAR(30),
    email VARCHAR(100)
);

INSERT INTO customers VALUES
(1, ' Arjun Rao ', 'Hyderabad', '98765-43210', ' ARJUN@GMAIL.COM '),
(2, 'SARA KHAN', 'Mumbai', '+91 99887 66554', 'sara@gmail.com'),
(3, 'Rohit Mehta ', 'Delhi', '9988 776 655', ''),
(4, 'Neha Singh', 'Hyderabad', '9876543210', 'neha@yahoo.com'),
(5, 'Imran Ali', 'Bangalore', '98765-AB210', NULL),
(6, 'Priya Nair', 'Pune', '9123456789', 'PRIYA@GMAIL.COM'),
(7, 'Kabir Shah', NULL, '9000011111', 'kabir@mail.com');

CREATE TABLE plans (
    plan_id INT PRIMARY KEY,
    plan_name VARCHAR(50),
    monthly_charge DECIMAL(10,2)
);

INSERT INTO plans VALUES
(101, 'Basic', 399),
(102, 'Standard', 599),
(103, 'Premium', 999),
(104, 'Unlimited', 1499),
(105, 'Business', 1999);

CREATE TABLE subscriptions (
    subscription_id INT PRIMARY KEY,
    customer_id INT,
    plan_id INT,
    start_date DATE,
    status VARCHAR(20)
);

INSERT INTO subscriptions VALUES
(1001, 1, 103, '2026-01-01', 'Active'),
(1002, 2, 102, '2026-01-15', 'Active'),
(1003, 3, 101, '2026-02-01', 'Inactive'),
(1004, 4, 104, '2026-02-10', 'Active'),
(1005, 5, 102, '2026-03-01', 'Active'),
(1006, 1, 105, '2026-04-01', 'Active'),
(1007, 6, NULL, '2026-04-15', 'Pending'),
(1008, 20, 103, '2026-05-01', 'Active');

CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    customer_id INT,
    payment_date DATE,
    amount DECIMAL(10,2)
);

INSERT INTO payments VALUES
(501, 1, '2026-01-05', 999),
(502, 2, '2026-01-18', 599),
(503, 1, '2026-02-05', 999),
(504, 3, '2026-02-10', 399),
(505, 4, '2026-02-15', 1499),
(506, 2, '2026-03-18', 599),
(507, 5, '2026-03-20', 599),
(508, 1, '2026-04-05', 1999),
(509, 4, '2026-04-15', 1499),
(510, 5, '2026-05-20', 599),
(511, 2, '2026-05-22', 599),
(512, 1, '2026-06-05', 1999);