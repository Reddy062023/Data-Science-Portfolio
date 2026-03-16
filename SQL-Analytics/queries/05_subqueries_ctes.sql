-- ─────────────────────────────────────────────────────────────────
-- 05: SUBQUERIES & CTEs
-- Covers: Subqueries in WHERE/FROM/SELECT, CTEs, recursive CTEs
-- ─────────────────────────────────────────────────────────────────

USE portfolio_analytics;

-- ── E-COMMERCE ───────────────────────────────────────────────────

-- 1. Customers who spent above average (subquery in WHERE)
SELECT
    c.first_name,
    c.last_name,
    SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING total_spent > (
    SELECT AVG(total_amount) FROM orders WHERE status = 'Completed'
)
ORDER BY total_spent DESC;

-- 2. Most popular product per category (CTE)
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(oi.quantity * oi.unit_price) AS revenue,
        RANK() OVER (
            PARTITION BY p.category
            ORDER BY SUM(oi.quantity * oi.unit_price) DESC
        ) AS rnk
    FROM products p
    INNER JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT category, product_name, revenue
FROM product_revenue
WHERE rnk = 1
ORDER BY revenue DESC;

-- 3. Customer order summary CTE
WITH customer_summary AS (
    SELECT
        c.customer_id,
        CONCAT(c.first_name,' ',c.last_name) AS customer_name,
        c.loyalty_tier,
        COUNT(o.order_id)                     AS total_orders,
        SUM(o.total_amount)                   AS total_spent,
        AVG(o.total_amount)                   AS avg_order
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.loyalty_tier
)
SELECT *,
    CASE
        WHEN total_spent > 1000 THEN 'High Value'
        WHEN total_spent > 500  THEN 'Medium Value'
        ELSE                         'Low Value'
    END AS customer_segment
FROM customer_summary
ORDER BY total_spent DESC;

-- ── HEALTHCARE ───────────────────────────────────────────────────

-- 4. Patients with above average admission cost (subquery)
SELECT
    CONCAT(p.first_name,' ',p.last_name) AS patient_name,
    a.diagnosis,
    a.total_cost
FROM patients p
INNER JOIN admissions a ON p.patient_id = a.patient_id
WHERE a.total_cost > (SELECT AVG(total_cost) FROM admissions)
ORDER BY a.total_cost DESC;

-- 5. High cost patients CTE
WITH patient_costs AS (
    SELECT
        p.patient_id,
        CONCAT(p.first_name,' ',p.last_name) AS patient_name,
        p.insurance_type,
        COUNT(a.admission_id)                AS admissions,
        SUM(a.total_cost)                    AS total_cost
    FROM patients p
    INNER JOIN admissions a ON p.patient_id = a.patient_id
    GROUP BY p.patient_id, p.first_name, p.last_name, p.insurance_type
),
avg_cost AS (
    SELECT AVG(total_cost) AS avg_patient_cost FROM patient_costs
)
SELECT
    pc.*,
    ROUND(pc.total_cost - ac.avg_patient_cost, 2) AS above_avg_by
FROM patient_costs pc
CROSS JOIN avg_cost ac
WHERE pc.total_cost > ac.avg_patient_cost
ORDER BY pc.total_cost DESC;

-- ── FINANCE ──────────────────────────────────────────────────────

-- 6. High risk borrowers (subquery)
SELECT
    CONCAT(b.first_name,' ',b.last_name) AS borrower_name,
    b.credit_score,
    b.income_annual,
    COUNT(l.loan_id)                     AS total_loans,
    SUM(l.defaulted)                     AS defaults
FROM borrowers b
INNER JOIN loans l ON b.borrower_id = l.borrower_id
WHERE b.credit_score < (
    SELECT AVG(credit_score) FROM borrowers
)
GROUP BY b.borrower_id, b.first_name, b.last_name,
         b.credit_score, b.income_annual
HAVING defaults > 0
ORDER BY defaults DESC;

-- 7. Loan risk analysis CTE
WITH loan_stats AS (
    SELECT
        loan_grade,
        COUNT(*)                             AS total_loans,
        SUM(defaulted)                       AS defaults,
        AVG(loan_amount)                     AS avg_amount,
        AVG(interest_rate)                   AS avg_rate
    FROM loans
    GROUP BY loan_grade
),
overall AS (
    SELECT AVG(CAST(defaulted AS DECIMAL)) * 100 AS overall_default_rate
    FROM loans
)
SELECT
    ls.*,
    ROUND(ls.defaults / ls.total_loans * 100, 2)   AS default_rate_pct,
    o.overall_default_rate,
    ROUND(ls.defaults / ls.total_loans * 100, 2)
        - o.overall_default_rate                   AS vs_overall
FROM loan_stats ls
CROSS JOIN overall o
ORDER BY default_rate_pct DESC;

-- ── HR ───────────────────────────────────────────────────────────

-- 8. Employees earning above department average (subquery)
SELECT
    e.first_name,
    e.last_name,
    e.job_title,
    e.salary,
    d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
)
ORDER BY d.department_name, e.salary DESC;

-- 9. Department performance CTE
WITH dept_stats AS (
    SELECT
        d.department_name,
        COUNT(e.employee_id)       AS headcount,
        AVG(e.salary)              AS avg_salary,
        AVG(e.performance_rating)  AS avg_rating,
        SUM(e.salary)              AS total_payroll
    FROM departments d
    INNER JOIN employees e ON d.department_id = e.department_id
    GROUP BY d.department_id, d.department_name
),
company_avg AS (
    SELECT
        AVG(salary)             AS company_avg_salary,
        AVG(performance_rating) AS company_avg_rating
    FROM employees
)
SELECT
    ds.*,
    ROUND(ds.avg_salary - ca.company_avg_salary, 2)   AS vs_company_salary,
    ROUND(ds.avg_rating - ca.company_avg_rating, 2)   AS vs_company_rating,
    CASE
        WHEN ds.avg_salary > ca.company_avg_salary
         AND ds.avg_rating > ca.company_avg_rating
        THEN 'High Performing'
        WHEN ds.avg_salary < ca.company_avg_salary
        THEN 'Below Average Pay'
        ELSE 'Average'
    END AS dept_status
FROM dept_stats ds
CROSS JOIN company_avg ca
ORDER BY ds.avg_salary DESC;