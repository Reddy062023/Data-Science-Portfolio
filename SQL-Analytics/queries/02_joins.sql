-- ─────────────────────────────────────────────────────────────────
-- 02: JOINS
-- Covers: INNER JOIN, LEFT JOIN, RIGHT JOIN, multiple joins
-- ─────────────────────────────────────────────────────────────────

USE portfolio_analytics;

-- ── E-COMMERCE ───────────────────────────────────────────────────

-- 1. Orders with customer names (INNER JOIN)
SELECT
    o.order_id,
    c.first_name,
    c.last_name,
    c.city,
    o.order_date,
    o.total_amount,
    o.status
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date;

-- 2. All customers including those with no orders (LEFT JOIN)
SELECT
    c.first_name,
    c.last_name,
    c.loyalty_tier,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.loyalty_tier
ORDER BY total_spent DESC;

-- 3. Order items with product details (multiple joins)
SELECT
    o.order_id,
    c.first_name,
    c.last_name,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total
FROM order_items oi
INNER JOIN orders o    ON oi.order_id   = o.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p  ON oi.product_id = p.product_id
ORDER BY o.order_id;

-- 4. Products never ordered (LEFT JOIN + NULL check)
SELECT p.product_name, p.category, p.unit_price
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;

-- ── HEALTHCARE ───────────────────────────────────────────────────

-- 5. Admissions with patient and doctor details
SELECT
    a.admission_id,
    CONCAT(p.first_name,' ',p.last_name) AS patient_name,
    p.age,
    p.insurance_type,
    CONCAT(d.first_name,' ',d.last_name) AS doctor_name,
    d.specialization,
    a.diagnosis,
    a.admission_date,
    a.discharge_date,
    a.total_cost,
    DATEDIFF(a.discharge_date, a.admission_date) AS days_admitted
FROM admissions a
INNER JOIN patients p ON a.patient_id = p.patient_id
INNER JOIN doctors  d ON a.doctor_id  = d.doctor_id
ORDER BY a.total_cost DESC;

-- 6. Doctors with no admissions (LEFT JOIN)
SELECT
    d.first_name,
    d.last_name,
    d.specialization,
    COUNT(a.admission_id) AS total_admissions
FROM doctors d
LEFT JOIN admissions a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
ORDER BY total_admissions DESC;

-- ── FINANCE ──────────────────────────────────────────────────────

-- 7. Loans with borrower details
SELECT
    l.loan_id,
    CONCAT(b.first_name,' ',b.last_name) AS borrower_name,
    b.credit_score,
    b.income_annual,
    b.employment_status,
    l.loan_amount,
    l.interest_rate,
    l.loan_grade,
    l.loan_purpose,
    l.status,
    l.defaulted
FROM loans l
INNER JOIN borrowers b ON l.borrower_id = b.borrower_id
ORDER BY l.loan_amount DESC;

-- 8. All borrowers including those with no loans (LEFT JOIN)
SELECT
    b.first_name,
    b.last_name,
    b.credit_score,
    COUNT(l.loan_id)        AS total_loans,
    COALESCE(SUM(l.loan_amount), 0) AS total_borrowed
FROM borrowers b
LEFT JOIN loans l ON b.borrower_id = l.borrower_id
GROUP BY b.borrower_id, b.first_name, b.last_name, b.credit_score
ORDER BY total_borrowed DESC;

-- ── HR ───────────────────────────────────────────────────────────

-- 9. Employees with department details
SELECT
    e.first_name,
    e.last_name,
    e.job_title,
    e.salary,
    e.hire_date,
    e.performance_rating,
    d.department_name,
    d.location
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
ORDER BY d.department_name, e.salary DESC;

-- 10. Employees with their manager names (SELF JOIN)
SELECT
    e.first_name                          AS employee_first,
    e.last_name                           AS employee_last,
    e.job_title,
    e.salary,
    CONCAT(m.first_name,' ',m.last_name)  AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY manager_name, e.salary DESC;