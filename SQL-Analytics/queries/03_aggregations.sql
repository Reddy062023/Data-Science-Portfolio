-- ─────────────────────────────────────────────────────────────────
-- 03: GROUP BY & AGGREGATIONS
-- Covers: COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING
-- ─────────────────────────────────────────────────────────────────

USE portfolio_analytics;

-- ── E-COMMERCE ───────────────────────────────────────────────────

-- 1. Revenue by product category
SELECT
    p.category,
    COUNT(oi.item_id)              AS total_items_sold,
    SUM(oi.quantity)               AS total_quantity,
    SUM(oi.quantity * oi.unit_price) AS total_revenue,
    AVG(oi.unit_price)             AS avg_price
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 2. Monthly revenue trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(order_id)                  AS total_orders,
    SUM(total_amount)                AS total_revenue,
    AVG(total_amount)                AS avg_order_value
FROM orders
WHERE status = 'Completed'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

-- 3. Revenue by customer loyalty tier
SELECT
    c.loyalty_tier,
    COUNT(DISTINCT c.customer_id)  AS customers,
    COUNT(o.order_id)              AS total_orders,
    SUM(o.total_amount)            AS total_revenue,
    AVG(o.total_amount)            AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.loyalty_tier
ORDER BY total_revenue DESC;

-- 4. Top customers by spend (HAVING)
SELECT
    c.first_name,
    c.last_name,
    COUNT(o.order_id)   AS total_orders,
    SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING total_spent > 500
ORDER BY total_spent DESC;

-- ── HEALTHCARE ───────────────────────────────────────────────────

-- 5. Total revenue by doctor
SELECT
    CONCAT(d.first_name,' ',d.last_name) AS doctor_name,
    d.specialization,
    COUNT(a.admission_id)                AS total_admissions,
    SUM(a.total_cost)                    AS total_revenue,
    AVG(a.total_cost)                    AS avg_cost,
    AVG(DATEDIFF(a.discharge_date, a.admission_date)) AS avg_stay_days
FROM doctors d
INNER JOIN admissions a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
ORDER BY total_revenue DESC;

-- 6. Admissions by insurance type
SELECT
    p.insurance_type,
    COUNT(a.admission_id) AS total_admissions,
    SUM(a.total_cost)     AS total_cost,
    AVG(a.total_cost)     AS avg_cost,
    MIN(a.total_cost)     AS min_cost,
    MAX(a.total_cost)     AS max_cost
FROM patients p
INNER JOIN admissions a ON p.patient_id = a.patient_id
GROUP BY p.insurance_type
ORDER BY total_cost DESC;

-- 7. Diagnosis frequency and avg cost
SELECT
    diagnosis,
    COUNT(*)          AS frequency,
    AVG(total_cost)   AS avg_cost,
    SUM(total_cost)   AS total_cost
FROM admissions
GROUP BY diagnosis
HAVING frequency > 1
ORDER BY avg_cost DESC;

-- ── FINANCE ──────────────────────────────────────────────────────

-- 8. Default rate by loan grade
SELECT
    loan_grade,
    COUNT(*)                          AS total_loans,
    SUM(defaulted)                    AS defaults,
    ROUND(SUM(defaulted)/COUNT(*)*100,2) AS default_rate_pct,
    AVG(loan_amount)                  AS avg_loan_amount,
    AVG(interest_rate)                AS avg_interest_rate
FROM loans
GROUP BY loan_grade
ORDER BY loan_grade;

-- 9. Total exposure by loan purpose
SELECT
    loan_purpose,
    COUNT(*)          AS total_loans,
    SUM(loan_amount)  AS total_exposure,
    AVG(loan_amount)  AS avg_loan,
    SUM(defaulted)    AS defaults
FROM loans
GROUP BY loan_purpose
ORDER BY total_exposure DESC;

-- 10. Borrower stats by employment status
SELECT
    b.employment_status,
    COUNT(DISTINCT b.borrower_id)     AS borrowers,
    AVG(b.credit_score)               AS avg_credit_score,
    AVG(b.income_annual)              AS avg_income,
    COUNT(l.loan_id)                  AS total_loans,
    SUM(l.defaulted)                  AS defaults
FROM borrowers b
LEFT JOIN loans l ON b.borrower_id = l.borrower_id
GROUP BY b.employment_status
ORDER BY defaults DESC;

-- ── HR ───────────────────────────────────────────────────────────

-- 11. Salary stats by department
SELECT
    d.department_name,
    COUNT(e.employee_id)  AS headcount,
    AVG(e.salary)         AS avg_salary,
    MIN(e.salary)         AS min_salary,
    MAX(e.salary)         AS max_salary,
    SUM(e.salary)         AS total_payroll
FROM departments d
INNER JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name
ORDER BY avg_salary DESC;

-- 12. Performance rating distribution
SELECT
    performance_rating,
    COUNT(*)        AS employees,
    AVG(salary)     AS avg_salary,
    MIN(salary)     AS min_salary,
    MAX(salary)     AS max_salary
FROM employees
GROUP BY performance_rating
ORDER BY performance_rating DESC;

-- 13. Departments with avg salary > 70000 (HAVING)
SELECT
    d.department_name,
    COUNT(e.employee_id) AS headcount,
    AVG(e.salary)        AS avg_salary
FROM departments d
INNER JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name
HAVING avg_salary > 70000
ORDER BY avg_salary DESC;