-- Database setup for Library Management System
CREATE DATABASE IF NOT EXISTS ots;
USE ots;

-- 1. Table for Books
CREATE TABLE IF NOT EXISTS books (
    id VARCHAR(20) PRIMARY KEY,
    bookname VARCHAR(100) NOT NULL,
    avability INT NOT NULL
);

-- 2. Table for Library Members
CREATE TABLE IF NOT EXISTS library (
    membership VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    doj DATE NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- 3. Table for Book Issues
CREATE TABLE IF NOT EXISTS issue (
    booking_date DATE NOT NULL,
    mem_id VARCHAR(20) NOT NULL,
    book_id VARCHAR(20) NOT NULL,
    due_date DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    token VARCHAR(20) NOT NULL,
    cost VARCHAR(20) NOT NULL
);

-- Sample Initial Books
INSERT IGNORE INTO books (id, bookname, avability) VALUES
('BO101', 'PYTHON PROGRAMMING', 5),
('BO102', 'DATA STRUCTURES', 3),
('BO103', 'LEARN SQL', 4);
