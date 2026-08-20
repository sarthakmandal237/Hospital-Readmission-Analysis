-- ============================================================
-- Phase 2: Business Queries
-- Hospital Readmission & Cost Leakage Analysis
-- All queries use plain SELECT / GROUP BY / ORDER BY (no CTEs,
-- no window functions, no subqueries) as requested.
-- ============================================================

USE hospital_readmission;

-- ------------------------------------------------------------
-- Q1. 30-day readmission rate by diagnosis category
-- Business question: which diagnosis groups drive the most
-- avoidable readmissions?
-- ------------------------------------------------------------
SELECT
    diagnosis_category,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30d) AS readmissions_30d,
    ROUND(SUM(readmitted_30d) / COUNT(*) * 100, 2) AS readmit_rate_pct
FROM patient_encounters
GROUP BY diagnosis_category
ORDER BY readmit_rate_pct DESC;


-- ------------------------------------------------------------
-- Q2. 30-day readmission rate by age group
-- Business question: which age segments are most at risk?
-- ------------------------------------------------------------
SELECT
    age,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30d) AS readmissions_30d,
    ROUND(SUM(readmitted_30d) / COUNT(*) * 100, 2) AS readmit_rate_pct
FROM patient_encounters
GROUP BY age
ORDER BY age;


-- ------------------------------------------------------------
-- Q3. 30-day readmission rate by admission type
-- Business question: do emergency admissions readmit more
-- than elective/urgent ones?
-- ------------------------------------------------------------
SELECT
    admission_type,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30d) AS readmissions_30d,
    ROUND(SUM(readmitted_30d) / COUNT(*) * 100, 2) AS readmit_rate_pct
FROM patient_encounters
GROUP BY admission_type
ORDER BY readmit_rate_pct DESC;


-- ------------------------------------------------------------
-- Q4. High-utilizer segment vs. everyone else
-- Business question: how much more likely are high utilizers
-- (prior ER/inpatient visits) to be readmitted?
-- ------------------------------------------------------------
SELECT
    high_utilizer,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30d) AS readmissions_30d,
    ROUND(SUM(readmitted_30d) / COUNT(*) * 100, 2) AS readmit_rate_pct
FROM patient_encounters
GROUP BY high_utilizer
ORDER BY high_utilizer DESC;


-- ------------------------------------------------------------
-- Q5. Total & average cost exposure by diagnosis category
-- Business question: where is the dollar exposure concentrated,
-- and which categories are the most expensive per readmission?
-- ------------------------------------------------------------
SELECT
    diagnosis_category,
    SUM(readmitted_30d) AS readmissions_30d,
    ROUND(SUM(CASE WHEN readmitted_30d = 1 THEN estimated_cost ELSE 0 END), 2) AS total_readmit_cost,
    ROUND(AVG(CASE WHEN readmitted_30d = 1 THEN estimated_cost END), 2) AS avg_cost_per_readmit
FROM patient_encounters
GROUP BY diagnosis_category
ORDER BY total_readmit_cost DESC;


-- ------------------------------------------------------------
-- Q6. Cost exposure by discharge disposition
-- Business question: are readmissions concentrated among
-- patients discharged to certain settings (e.g. home vs. SNF)?
-- ------------------------------------------------------------
SELECT
    discharge_disposition,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30d) AS readmissions_30d,
    ROUND(SUM(readmitted_30d) / COUNT(*) * 100, 2) AS readmit_rate_pct,
    ROUND(SUM(CASE WHEN readmitted_30d = 1 THEN estimated_cost ELSE 0 END), 2) AS total_readmit_cost
FROM patient_encounters
GROUP BY discharge_disposition
ORDER BY total_readmit_cost DESC
LIMIT 10;


-- ------------------------------------------------------------
-- Q7. Overall cost leakage summary (single-row KPI query)
-- Business question: what's the headline number for finance -
-- total estimated cost exposure tied to avoidable 30-day
-- readmissions across the whole hospital system?
-- ------------------------------------------------------------
SELECT
    COUNT(*) AS total_encounters,
    SUM(readmitted_30d) AS total_readmissions_30d,
    ROUND(SUM(readmitted_30d) / COUNT(*) * 100, 2) AS overall_readmit_rate_pct,
    ROUND(SUM(CASE WHEN readmitted_30d = 1 THEN estimated_cost ELSE 0 END), 2) AS total_cost_exposure,
    ROUND(AVG(CASE WHEN readmitted_30d = 1 THEN estimated_cost END), 2) AS avg_cost_per_readmission
FROM patient_encounters;