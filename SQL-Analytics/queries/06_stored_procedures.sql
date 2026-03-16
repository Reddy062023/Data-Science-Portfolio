-- ─────────────────────────────────────────────────────────────────
-- 06: STORED PROCEDURES
-- Covers: CREATE PROCEDURE, IN/OUT parameters, IF/ELSE, LOOP
-- ─────────────────────────────────────────────────────────────────

USE portfolio_analytics;

-- ─────────────────────────────────────────────────────────────────
-- E-COMMERCE PROCEDURES
-- ─────────────────────────────────────────────────────────────────

-- 1. Get customer order summary
DROP PROCEDURE IF EXISTS GetCustomerSummary;
DELIMITER $$
CREATE PROCEDURE GetCustomerSummary(IN p_customer_id INT)
BEGIN
    SELECT
        CONCAT(c.first_name,' ',c.last_name) AS customer_name,
        c.loyalty_tier,
        c.city,
        c.country,
        COUNT(o.order_id)                     AS total_orders,
        SUM(o.total_amount)                   AS total_spent,
        AVG(o.total_amount)                   AS avg_order_value,
        MIN(o.order_date)                     AS first_order,
        MAX(o.order_date)                     AS last_order
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.customer_id = p_customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name,
             c.loyalty_tier, c.city, c.country;
END$$
DELIMITER ;

-- Test it
CALL GetCustomerSummary(1);
CALL GetCustomerSummary(2);

-- ─────────────────────────────────────────────────────────────────
-- HEALTHCARE PROCEDURES
-- ─────────────────────────────────────────────────────────────────

-- 2. Get patient admission history
DROP PROCEDURE IF EXISTS GetPatientHistory;
DELIMITER $$
CREATE PROCEDURE GetPatientHistory(IN p_patient_id INT)
BEGIN
    SELECT
        CONCAT(p.first_name,' ',p.last_name)  AS patient_name,
        p.age,
        p.insurance_type,
        a.admission_date,
        a.discharge_date,
        DATEDIFF(a.discharge_date, a.admission_date) AS days_admitted,
        a.diagnosis,
        CONCAT(d.first_name,' ',d.last_name)  AS doctor_name,
        d.specialization,
        a.total_cost
    FROM patients p
    INNER JOIN admissions a ON p.patient_id = a.patient_id
    INNER JOIN doctors    d ON a.doctor_id  = d.doctor_id
    WHERE p.patient_id = p_patient_id
    ORDER BY a.admission_date;
END$$
DELIMITER ;

-- Test it
CALL GetPatientHistory(1);
CALL GetPatientHistory(5);

-- ─────────────────────────────────────────────────────────────────
-- FINANCE PROCEDURES
-- ─────────────────────────────────────────────────────────────────

-- 3. Get loan default risk assessment
DROP PROCEDURE IF EXISTS AssessLoanRisk;
DELIMITER $$
CREATE PROCEDURE AssessLoanRisk(
    IN  p_credit_score  INT,
    IN  p_loan_amount   DECIMAL(12,2),
    IN  p_income_annual DECIMAL(12,2),
    OUT p_risk_level    VARCHAR(20),
    OUT p_recommendation VARCHAR(50)
)
BEGIN
    DECLARE v_dti DECIMAL(10,4);
    SET v_dti = p_loan_amount / p_income_annual;

    IF p_credit_score >= 750 AND v_dti < 0.3 THEN
        SET p_risk_level    = 'LOW';
        SET p_recommendation = 'Approve — Excellent profile';
    ELSEIF p_credit_score >= 700 AND v_dti < 0.4 THEN
        SET p_risk_level    = 'MEDIUM';
        SET p_recommendation = 'Approve with standard terms';
    ELSEIF p_credit_score >= 650 AND v_dti < 0.5 THEN
        SET p_risk_level    = 'HIGH';
        SET p_recommendation = 'Review — Consider higher rate';
    ELSE
        SET p_risk_level    = 'VERY HIGH';
        SET p_recommendation = 'Decline — Too risky';
    END IF;
END$$
DELIMITER ;

-- Test it
CALL AssessLoanRisk(760, 15000, 95000, @risk, @rec);
SELECT @risk AS risk_level, @rec AS recommendation;

CALL AssessLoanRisk(580, 8000, 35000, @risk, @rec);
SELECT @risk AS risk_level, @rec AS recommendation;

-- ─────────────────────────────────────────────────────────────────
-- HR PROCEDURES
-- ─────────────────────────────────────────────────────────────────

-- 4. Get department headcount and payroll report
DROP PROCEDURE IF EXISTS GetDeptReport;
DELIMITER $$
CREATE PROCEDURE GetDeptReport(IN p_department_name VARCHAR(50))
BEGIN
    IF p_department_name = 'ALL' THEN
        SELECT
            d.department_name,
            d.location,
            COUNT(e.employee_id)      AS headcount,
            AVG(e.salary)             AS avg_salary,
            SUM(e.salary)             AS total_payroll,
            AVG(e.performance_rating) AS avg_rating
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name, d.location
        ORDER BY total_payroll DESC;
    ELSE
        SELECT
            e.first_name,
            e.last_name,
            e.job_title,
            e.salary,
            e.hire_date,
            e.performance_rating
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.department_id
        WHERE d.department_name = p_department_name
        ORDER BY e.salary DESC;
    END IF;
END$$
DELIMITER ;

-- Test it
CALL GetDeptReport('ALL');
CALL GetDeptReport('Engineering');
CALL GetDeptReport('Sales');

-- 5. Give salary raise to top performers
DROP PROCEDURE IF EXISTS GiveSalaryRaise;
DELIMITER $$
CREATE PROCEDURE GiveSalaryRaise(
    IN p_department_id INT,
    IN p_raise_pct     DECIMAL(5,2)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;

    -- Count eligible employees
    SELECT COUNT(*) INTO v_count
    FROM employees
    WHERE department_id    = p_department_id
      AND performance_rating = 5;

    IF v_count = 0 THEN
        SELECT 'No top performers found in this department' AS message;
    ELSE
        -- Show before
        SELECT
            first_name, last_name, salary AS current_salary,
            ROUND(salary * (1 + p_raise_pct/100), 2) AS new_salary
        FROM employees
        WHERE department_id    = p_department_id
          AND performance_rating = 5;

        SELECT CONCAT(v_count,' employees eligible for ',
                      p_raise_pct,'% raise') AS summary;
    END IF;
END$$
DELIMITER ;

-- Test it
CALL GiveSalaryRaise(1, 10.0);
CALL GiveSalaryRaise(3, 8.5);
