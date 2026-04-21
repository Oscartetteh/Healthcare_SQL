-- raw_data_extract.sql
-- Final raw data extract for Module 05 ETL
-- Combines patient, appointment, billing, doctor, and department data

SELECT
    p.patient_id,
    p.first_name AS patient_first_name,
    p.last_name AS patient_last_name,
    p.date_of_birth,
    p.gender,
    p.blood_type,
    p.email AS patient_email,
    p.phone AS patient_phone,
    p.city,
    p.insurance_type,
    p.registered_at,

    a.appointment_id,
    a.appointment_date,
    a.appointment_time,
    a.status AS appointment_status,
    a.visit_type,
    a.duration_mins,
    a.fee AS appointment_fee,
    a.notes,

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
    d.dept_id AS doctor_dept_id,
    d.years_exp,
    d.salary,
    d.email AS doctor_email,
    d.phone AS doctor_phone,
    d.hire_date,
    d.is_active,

    dept.dept_id,
    dept.dept_name,
    dept.floor_number,
    dept.head_doctor,
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

ORDER BY
    p.patient_id,
    a.appointment_date,
    a.appointment_time;