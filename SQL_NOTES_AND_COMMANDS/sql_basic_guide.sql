-- ==============================================================================
-- SQL COMMANDS & CONCEPTS CHEATSHEET
-- Categories: DDL, DML, TCL
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. TYPES OF COMMANDS IN SQL:
-- DDL => Data Definition Language
-- DML => Data Manipulation Language
-- TCL => Transaction Control Language
--
-- DDL COMMAND: All commands related to creating, modifying, or removing 
-- the structure of the database (e.g. CREATE, ALTER, DROP).
--
-- DML COMMAND: All commands related to manipulating data inside tables 
-- (e.g. INSERT, UPDATE, DELETE, SELECT).
--
-- TCL COMMAND: All commands related to controlling transactions 
-- (e.g. COMMIT, ROLLBACK, SAVEPOINT).
-- ------------------------------------------------------------------------------

-- ------------------------------------------------------------------------------
-- 2. DATA TYPES IN SQL:
-- CHAR(size)      => Fixed character length data (faster, can waste memory)
-- VARCHAR(size)   => Variable character length data (saves memory)
-- NUMERIC/INT     => Numeric / Integer data
-- DECIMAL(M, D)   => Exact decimal numbers (e.g. currency, fees)
-- BOOLEAN         => Logical TRUE / FALSE values
-- DATE            => Dates in 'YYYY-MM-DD' format
-- BLOB            => Binary Large Objects (e.g. images, audio, documents)
-- ------------------------------------------------------------------------------

-- ------------------------------------------------------------------------------
-- 3. CORE SQL COMMANDS WITH EXAMPLES:
-- ------------------------------------------------------------------------------

-- Create a Database:
CREATE DATABASE IF NOT EXISTS school_management;

-- View List of Databases:
SHOW DATABASES;

-- Open / Select a Database:
USE school_management;

-- Create Table:
CREATE TABLE IF NOT EXISTS student (
    eno INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    course VARCHAR(50) NOT NULL,
    fees DECIMAL(10, 2) NOT NULL
);

-- View List of Tables in Database:
SHOW TABLES;

-- View Table Structure:
DESC student;

-- Insert Records (DML):
INSERT INTO student (eno, name, course, fees) VALUES 
(101, 'Shaurya', 'Python', 15000),
(102, 'Rohan', 'Data Science', 20000),
(103, 'Aman', 'Web Development', 18000);

-- Display Records:
SELECT * FROM student;

-- Search Record:
SELECT * FROM student WHERE eno = 101;

-- Update Record:
UPDATE student SET course = 'Full Stack Python', fees = 16000 WHERE eno = 101;

-- Delete Record:
DELETE FROM student WHERE eno = 103;

-- Save Changes:
COMMIT;

-- Drop Table:
-- DROP TABLE student;

-- Drop Database:
-- DROP DATABASE school_management;
