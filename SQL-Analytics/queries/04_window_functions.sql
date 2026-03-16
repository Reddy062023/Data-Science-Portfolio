-- ─────────────────────────────────────────────────────────────────
-- 04: WINDOW FUNCTIONS
-- Covers: RANK, DENSE_RANK, ROW_NUMBER, LAG, LEAD,
--         SUM OVER, AVG OVER, PARTITION BY
-- ─────────────────────────────────────────────────────────────────

USE portfolio_analytics;

-- ── E-COMMERCE ───────────────────────────────────────────────────

-- 1. Rank customers by total spend
SELECT
    c.first_name,
    c.last_name,
    c.loyalty_tier,
    SUM(o.total_amount)                               AS total_spent,
    RANK() OVER (ORDER BY SUM(o.total_amount) DESC)   AS spend_rank,
    DENSE_RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS dense_rank
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name, c.loyalty_tier;

-- 2. Rank products by revenue within each category
SELECT
    p.category,
    p.product_name,
    SUM(oi.quantity * oi.unit_price)                  AS total_revenue,
    RANK() OVER (
        PARTITION BY p.category
        ORDER BY SUM(oi.quantity * oi.unit_price) DESC
    ) AS rank_in_category
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.category, p.product_name;

-- 3. Running total revenue by month
SELECT
    DATE_FORMAT(order_date,'%Y-%m')                       AS month,
    SUM(total_amount)                                     AS monthly_revenue,
    SUM(SUM(total_amount)) OVER (
        ORDER BY DATE_FORMAT(order_date,'%Y-%m')
    )                                                     AS running_total
FROM orders
WHERE status = 'Completed'
GROUP BY DATE_FORMAT(order_date,'%Y-%m')
ORDER BY month;

-- 4. Month over month revenue change (LAG)
SELECT
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month)            AS prev_month_revenue,
    ROUND(monthly_revenue -
          LAG(monthly_revenue) OVER (ORDER BY month), 2)  AS revenue_change
FROM (
    SELECT
        DATE_FORMAT(order_date,'%Y-%m') AS month,
        SUM(total_amount)               AS monthly_revenue
    FROM orders
    WHERE status = 'Completed'
    GROUP BY DATE_FORMAT(order_date,'%Y-%m')
) monthly
ORDER BY month;

-- ── HEALTHCARE ───────────────────────────────────────────────────

-- 5. Rank patients by total admission cost
SELECT
    CONCAT(p.first_name,' ',p.last_name)               AS patient_name,
    p.insurance_type,
    SUM(a.total_cost)                                  AS total_cost,
    RANK() OVER (ORDER BY SUM(a.total_cost) DESC)      AS cost_rank,
    ROW_NUMBER() OVER (ORDER BY SUM(a.total_cost) DESC) AS row_num
FROM patients p
INNER JOIN admissions a ON p.patient_id = a.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name, p.insurance_type;

-- 6. Running total cost by doctor
SELECT
    CONCAT(d.first_name,' ',d.last_name)  AS doctor_name,
    a.admission_date,
    a.total_cost,
    SUM(a.total_cost) OVER (
        PARTITION BY d.doctor_id
        ORDER BY a.admission_date
    )                                     AS running_total_by_doctor
FROM doctors d
INNER JOIN admissions a ON d.doctor_id = a.doctor_id
ORDER BY d.doctor_id, a.admission_date;

-- ── FINANCE ──────────────────────────────────────────────────────

-- 7. Rank borrowers by credit score within employment status
SELECT
    CONCAT(b.first_name,' ',b.last_name)              AS borrower_name,
    b.employment_status,
    b.credit_score,
    b.income_annual,
    RANK() OVER (
        PARTITION BY b.employment_status
        ORDER BY b.credit_score DESC
    )                                                 AS rank_in_group,
    AVG(b.credit_score) OVER (
        PARTITION BY b.employment_status
    )                                                 AS avg_score_in_group
FROM borrowers b;

-- 8. Loan amount vs average by grade
SELECT
    loan_id,
    loan_grade,
    loan_amount,
    AVG(loan_amount) OVER (
        PARTITION BY loan_grade
    )                                                 AS avg_amount_in_grade,
    loan_amount - AVG(loan_amount) OVER (
        PARTITION BY loan_grade
    )                                                 AS diff_from_avg
FROM loans
ORDER BY loan_grade, loan_amount DESC;

-- ── HR ───────────────────────────────────────────────────────────

-- 9. Rank employees by salary within department
SELECT
    CONCAT(e.first_name,' ',e.last_name)              AS employee_name,
    d.department_name,
    e.job_title,
    e.salary,
    RANK() OVER (
        PARTITION BY e.department_id
        ORDER BY e.salary DESC
    )                                                 AS salary_rank,
    AVG(e.salary) OVER (
        PARTITION BY e.department_id
    )                                                 AS dept_avg_salary,
    e.salary - AVG(e.salary) OVER (
        PARTITION BY e.department_id
    )                                                 AS diff_from_dept_avg
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
ORDER BY d.department_name, salary_rank;

-- 10. Employee salary history with LEAD
SELECT
    e.first_name,
    e.last_name,
    s.effective_date,
    s.salary,
    LEAD(s.salary) OVER (
        PARTITION BY s.employee_id
        ORDER BY s.effective_date
    )                                                 AS next_salary,
    LEAD(s.salary) OVER (
        PARTITION BY s.employee_id
        ORDER BY s.effective_date
    ) - s.salary                                      AS salary_increase
FROM salaries s
INNER JOIN employees e ON s.employee_id = e.employee_id
ORDER BY e.employee_id, s.effective_date;