-- Database setup for Bank Management System
CREATE DATABASE IF NOT EXISTS ots;
USE ots;

CREATE TABLE IF NOT EXISTS customer (
    acc INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(30) NOT NULL,
    bal INT NOT NULL
);

-- Sample Customers
INSERT IGNORE INTO customer (acc, name, type, bal) VALUES
(1001, 'Shaurya Bhatia', 'Savings', 50000),
(1002, 'Rohan Verma', 'Current', 75000),
(1003, 'Aman Sharma', 'Savings', 30000);
