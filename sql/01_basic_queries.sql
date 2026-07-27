-- Query 1: Total Number of Admissions
SELECT
    COUNT(*) AS total_admissions
FROM admissions;

-- Query 2: Total Number of Patients
SELECT
    COUNT(DISTINCT patient_id) AS total_patients
FROM patients;

-- Query 3: Total Number of Hospitals
SELECT
    COUNT(*) AS total_hospitals
FROM hospitals;

-- Query 4: Total Number of Diagnosis Records
SELECT
    COUNT(*) AS total_diagnoses
FROM diagnoses;

-- Query 5: Average Length of Stay
SELECT
    ROUND(AVG(los_days),2) AS average_length_of_stay
FROM admissions;

-- Query 6: Minimum, Maximum and Average Length of Stay
SELECT

    MIN(los_days) AS minimum_los,

    MAX(los_days) AS maximum_los,

    ROUND(AVG(los_days),2) AS average_los

FROM admissions;

-- Query 7: Overall 30-Day Readmission Rate
SELECT

    ROUND(
        AVG(readmitted_30d) * 100,
        2
    ) AS readmission_rate_percent

FROM admissions;

-- Query 8: Average Number of Procedures
SELECT

    ROUND(
        AVG(num_procedures),
        2
    ) AS average_procedures

FROM admissions;

-- Query 9: Average Charlson Comorbidity Index
SELECT

    ROUND(
        AVG(charlson_index),
        2
    ) AS average_charlson_index

FROM admissions;

-- Query 10: Admission Type Distribution
SELECT

    admit_type,

    COUNT(*) AS total_admissions

FROM admissions

GROUP BY admit_type

ORDER BY total_admissions DESC;

-- Query 11: Ward Distribution
SELECT

    ward_type,

    COUNT(*) AS total_patients

FROM admissions

GROUP BY ward_type

ORDER BY total_patients DESC;

-- Query 12: Discharge Type Distribution
SELECT

    discharge_type,

    COUNT(*) AS total

FROM admissions

GROUP BY discharge_type

ORDER BY total DESC;

-- Query 13: Gender Distribution
SELECT

    gender,

    COUNT(*) AS total_patients

FROM patients

GROUP BY gender

ORDER BY total_patients DESC;

-- Query 14: Insurance Type Distribution
SELECT

    insurance_type,

    COUNT(*) AS total_patients

FROM patients

GROUP BY insurance_type

ORDER BY total_patients DESC;

-- Query 15: Hospital Tier Distribution
SELECT

    tier,

    COUNT(*) AS total_hospitals

FROM hospitals

GROUP BY tier

ORDER BY total_hospitals DESC;

-- Query 16: Average Hospital Cost
SELECT

    ROUND(
        AVG(total_cost_inr),
        2
    ) AS average_cost

FROM billing;

-- Query 17: Total Hospital Revenue
SELECT

    ROUND(
        SUM(total_cost_inr),
        2
    ) AS total_revenue

FROM billing;

-- Query 18: Cost Category Distribution
SELECT

    cost_category,

    COUNT(*) AS total_records

FROM billing

GROUP BY cost_category

ORDER BY total_records DESC;

-- Query 19: Top 10 Hospitals by Admissions
SELECT

    h.name,

    COUNT(*) AS admissions

FROM admissions a

JOIN hospitals h

ON a.hospital_id = h.hospital_id

GROUP BY h.name

ORDER BY admissions DESC

LIMIT 10;

-- Query 20: Top 10 States by Patient Count
SELECT

    state,

    COUNT(*) AS patients

FROM patients

GROUP BY state

ORDER BY patients DESC

LIMIT 10;