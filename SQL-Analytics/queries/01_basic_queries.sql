-- ─────────────────────────────────────────────────────────────────
-- 01: BASIC QUERIES
-- Covers: SELECT, WHERE, ORDER BY, LIMIT, DISTINCT
-- ─────────────────────────────────────────────────────────────────

USE portfolio_analytics;

-- ── E-COMMERCE ───────────────────────────────────────────────────

-- 1. All customers
SELECT * FROM customers;

-- 2. Customers from USA only
SELECT first_name, last_name, city
FROM customers
WHERE country = 'USA';

-- 3. Gold tier customers
SELECT first_name, last_name, email, loyalty_tier
FROM customers
WHERE loyalty_tier = 'Gold'
ORDER BY last_name;

-- 4. Top 5 most expensive products
SELECT product_name, category, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 5;

-- 5. Distinct product categories
SELECT DISTINCT category FROM products;

-- 6. Completed orders only
SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE status = 'Completed'
ORDER BY total_amount DESC;

-- ── HEALTHCARE ───────────────────────────────────────────────────

-- 7. All male patients
SELECT first_name, last_name, age, blood_type
FROM patients
WHERE gender = 'Male'
ORDER BY age DESC;

-- 8. Admissions with cost > 5000
SELECT admission_id, patient_id, diagnosis, total_cost
FROM admissions
WHERE total_cost > 5000
ORDER BY total_cost DESC;

-- 9. Patients with Medicare insurance
SELECT first_name, last_name, age, insurance_type
FROM patients
WHERE insurance_type = 'Medicare';

-- ── FINANCE ──────────────────────────────────────────────────────

-- 10. All defaulted loans
SELECT loan_id, borrower_id, loan_amount, loan_grade, status
FROM loans
WHERE defaulted = 1;

-- 11. Loans with interest rate > 10%
SELECT loan_id, loan_amount, interest_rate, loan_purpose
FROM loans
WHERE interest_rate > 10
ORDER BY interest_rate DESC;

-- 12. Grade A loans only
SELECT loan_id, borrower_id, loan_amount, interest_rate
FROM loans
WHERE loan_grade = 'A'
ORDER BY loan_amount DESC;

-- ── HR ───────────────────────────────────────────────────────────

-- 13. All employees with salary > 80000
SELECT first_name, last_name, job_title, salary
FROM employees
WHERE salary > 80000
ORDER BY salary DESC;

-- 14. Employees hired after 2021
SELECT first_name, last_name, hire_date, job_title
FROM employees
WHERE hire_date > '2021-01-01'
ORDER BY hire_date;

-- 15. Top rated employees (rating = 5)
SELECT first_name, last_name, job_title, performance_rating
FROM employees
WHERE performance_rating = 5
ORDER BY salary DESC;