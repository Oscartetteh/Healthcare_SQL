-- 02_aggregation.sql
-- Aggregation queries for the healthcare schema

SELECT
    gender,
    COUNT(*) AS total_patients
FROM healthcare.patients
GROUP BY gender
ORDER BY total_patients DESC;

SELECT
    insurance_type,
    COUNT(*) AS total_patients
FROM healthcare.patients
GROUP BY insurance_type
ORDER BY total_patients DESC;

SELECT
    status AS appointment_status,
    COUNT(*) AS total_appointments
FROM healthcare.appointments
GROUP BY status
ORDER BY total_appointments DESC;

SELECT
    visit_type,
    COUNT(*) AS total_appointments
FROM healthcare.appointments
GROUP BY visit_type
ORDER BY total_appointments DESC;

SELECT
    payment_status,
    COUNT(*) AS total_bills,
    SUM(amount_charged) AS total_amount_charged,
    SUM(insurance_paid) AS total_insurance_paid,
    SUM(patient_paid) AS total_patient_paid,
    AVG(amount_charged) AS average_amount_charged
FROM healthcare.billing
GROUP BY payment_status
ORDER BY total_amount_charged DESC;

SELECT
    dept.dept_name,
    COUNT(d.doctor_id) AS total_doctors
FROM healthcare.departments dept
LEFT JOIN healthcare.doctors d
    ON dept.dept_id = d.dept_id
GROUP BY dept.dept_name
ORDER BY total_doctors DESC;