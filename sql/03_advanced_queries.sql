-- Query 1: Rank Hospitals by Revenue
SELECT

    h.name,

    ROUND(SUM(b.total_cost_inr),2) AS revenue,

    RANK() OVER(
        ORDER BY SUM(b.total_cost_inr) DESC
    ) AS revenue_rank

FROM admissions a

JOIN hospitals h
ON a.hospital_id = h.hospital_id

JOIN billing b
ON a.admission_id = b.admission_id

GROUP BY h.name;

-- Query 2: Top 5 Hospitals by Readmission Rate
SELECT *

FROM(

SELECT

    h.name,

    ROUND(AVG(a.readmitted_30d)*100,2)
        AS readmission_rate,

    ROW_NUMBER() OVER(

        ORDER BY AVG(a.readmitted_30d) DESC

    ) AS row_num

FROM admissions a

JOIN hospitals h
ON a.hospital_id=h.hospital_id

GROUP BY h.name

)

WHERE row_num<=5;

-- Query 3: Revenue Contribution (%) by Hospital
SELECT

    h.name,

    ROUND(SUM(b.total_cost_inr),2)
        AS revenue,

    ROUND(

        SUM(b.total_cost_inr)

        *100.0/

        SUM(SUM(b.total_cost_inr))
        OVER(),

        2

    ) AS revenue_percentage

FROM admissions a

JOIN hospitals h
ON a.hospital_id=h.hospital_id

JOIN billing b
ON a.admission_id=b.admission_id

GROUP BY h.name

ORDER BY revenue DESC;

-- Query 4: Hospital Performance Category
SELECT

    h.name,

    ROUND(AVG(a.readmitted_30d)*100,2)
        AS readmission_rate,

    CASE

        WHEN AVG(a.readmitted_30d)<0.10
            THEN 'Excellent'

        WHEN AVG(a.readmitted_30d)<0.15
            THEN 'Good'

        ELSE 'Needs Improvement'

    END AS performance

FROM admissions a

JOIN hospitals h
ON a.hospital_id=h.hospital_id

GROUP BY h.name;

-- Query 5: Hospitals Having More Than 5000 Admissions
SELECT

    h.name,

    COUNT(*) AS admissions

FROM admissions a

JOIN hospitals h
ON a.hospital_id=h.hospital_id

GROUP BY h.name

HAVING COUNT(*)>5000

ORDER BY admissions DESC;

-- Query 6: Top Diagnosis Category in Each Hospital
WITH diagnosis_counts AS(

SELECT

    h.name,

    d.diag_category,

    COUNT(*) AS total_cases,

    ROW_NUMBER() OVER(

        PARTITION BY h.name

        ORDER BY COUNT(*) DESC

    ) AS rn

FROM admissions a

JOIN hospitals h
ON a.hospital_id=h.hospital_id

JOIN diagnoses d
ON a.admission_id=d.admission_id

GROUP BY h.name,d.diag_category

)

SELECT *

FROM diagnosis_counts

WHERE rn=1;

-- Query 7: Dense Rank Hospitals by Average LOS
SELECT

    h.name,

    ROUND(AVG(a.los_days),2)
        AS avg_los,

    DENSE_RANK() OVER(

        ORDER BY AVG(a.los_days) DESC

    ) AS los_rank

FROM admissions a

JOIN hospitals h
ON a.hospital_id=h.hospital_id

GROUP BY h.name;

-- Query 8: Patients with Multiple Admissions
SELECT

    patient_id,

    COUNT(*) AS admissions

FROM admissions

GROUP BY patient_id

HAVING COUNT(*)>1

ORDER BY admissions DESC;

-- Query 9: Above Average Cost Admissions
SELECT

    admission_id,

    total_cost_inr

FROM billing

WHERE total_cost_inr>

(

SELECT AVG(total_cost_inr)

FROM billing

);

-- Query 10: Running Revenue Trend
WITH monthly_revenue AS(

SELECT

    strftime('%Y-%m',a.admit_date)
        AS month,

    SUM(b.total_cost_inr)
        AS revenue

FROM admissions a

JOIN billing b

ON a.admission_id=b.admission_id

GROUP BY month

)

SELECT

    month,

    revenue,

    SUM(revenue)

    OVER(

        ORDER BY month

    ) AS cumulative_revenue

FROM monthly_revenue;

-- Query 11: Hospital Revenue Compared to Overall Average
WITH hospital_revenue AS(

SELECT

    h.name,

    SUM(b.total_cost_inr)
        AS revenue

FROM admissions a

JOIN hospitals h
ON a.hospital_id=h.hospital_id

JOIN billing b
ON a.admission_id=b.admission_id

GROUP BY h.name

)

SELECT

    name,

    ROUND(revenue,2),

    ROUND(

        (SELECT AVG(revenue)

        FROM hospital_revenue),

        2

    ) AS average_revenue

FROM hospital_revenue;

-- Query 12: Top 3 Hospitals in Every Tier
WITH ranked_hospitals AS(

SELECT

    h.tier,

    h.name,

    SUM(b.total_cost_inr)
        AS revenue,

    ROW_NUMBER() OVER(

        PARTITION BY h.tier

        ORDER BY SUM(b.total_cost_inr) DESC

    ) AS rank_in_tier

FROM admissions a

JOIN hospitals h
ON a.hospital_id=h.hospital_id

JOIN billing b
ON a.admission_id=b.admission_id

GROUP BY h.tier,h.name

)

SELECT *

FROM ranked_hospitals

WHERE rank_in_tier<=3;