-- 01_basics.sql
-- Basic checks against the healthcare schema

SELECT *
FROM healthcare.patients
LIMIT 10;

SELECT *
FROM healthcare.appointments
LIMIT 10;

SELECT *
FROM healthcare.billing
LIMIT 10;

SELECT *
FROM healthcare.doctors
LIMIT 10;

SELECT *
FROM healthcare.departments
LIMIT 10;
