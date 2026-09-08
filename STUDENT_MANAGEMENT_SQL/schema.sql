-- Database setup for Student Management System
CREATE DATABASE IF NOT EXISTS ots;
USE ots;

CREATE TABLE IF NOT EXISTS student (
    eno INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    course VARCHAR(50) NOT NULL,
    fees DECIMAL(10, 2) NOT NULL
);

-- Sample Data
INSERT IGNORE INTO student (eno, name, course, fees) VALUES
(101, 'Shaurya', 'Python', 15000),
(102, 'Aman', 'Data Science', 20000),
(103, 'Rohit', 'Web Development', 18000);
