-- 03_joins.sql
-- Joined extract using patients, appointments, billing, doctors, and departments

SELECT
    p.patient_id,
    p.first_name AS patient_first_name,
    p.last_name AS patient_last_name,
    p.gender,
    p.date_of_birth,
    p.insurance_type,

    a.appointment_id,
    a.appointment_date,
    a.appointment_time,
    a.status AS appointment_status,
    a.visit_type,
    a.duration_mins,
    a.fee AS appointment_fee,

    b.bill_id,
    b.amount_charged,
    b.insurance_paid,
    b.patient_paid,
    b.payment_status,
    b.bill_date,
    b.payment_method,

    d.doctor_id,
    d.first_name AS doctor_first_name,
    d.last_name AS doctor_last_name,
    d.specialization,

    dept.dept_id,
    dept.dept_name,
    dept.floor_number,
    dept.bed_count

FROM healthcare.patients p
LEFT JOIN healthcare.appointments a
    ON p.patient_id = a.patient_id
LEFT JOIN healthcare.billing b
    ON a.appointment_id = b.appointment_id
LEFT JOIN healthcare.doctors d
    ON a.doctor_id = d.doctor_id
LEFT JOIN healthcare.departments dept
    ON d.dept_id = dept.dept_id
LIMIT 100;