-- 04_cte_window.sql
-- CTE and window function example

WITH patient_billing AS (
    SELECT
        p.patient_id,
        p.first_name AS patient_first_name,
        p.last_name AS patient_last_name,
        p.gender,
        p.insurance_type,

        a.appointment_id,
        a.appointment_date,
        a.appointment_time,
        a.status AS appointment_status,
        a.visit_type,

        b.bill_id,
        b.amount_charged,
        b.insurance_paid,
        b.patient_paid,
        b.payment_status

    FROM healthcare.patients p
    LEFT JOIN healthcare.appointments a
        ON p.patient_id = a.patient_id
    LEFT JOIN healthcare.billing b
        ON a.appointment_id = b.appointment_id
)

SELECT
    patient_id,
    patient_first_name,
    patient_last_name,
    gender,
    insurance_type,
    appointment_id,
    appointment_date,
    appointment_time,
    appointment_status,
    visit_type,
    bill_id,
    amount_charged,
    insurance_paid,
    patient_paid,
    payment_status,

    SUM(amount_charged) OVER (
        PARTITION BY patient_id
    ) AS total_amount_charged_by_patient,

    SUM(insurance_paid) OVER (
        PARTITION BY patient_id
    ) AS total_insurance_paid_by_patient,

    SUM(patient_paid) OVER (
        PARTITION BY patient_id
    ) AS total_patient_paid_by_patient,

    ROW_NUMBER() OVER (
        PARTITION BY patient_id
        ORDER BY appointment_date DESC, appointment_time DESC
    ) AS appointment_rank_for_patient

FROM patient_billing
ORDER BY
    patient_id,
    appointment_rank_for_patient;