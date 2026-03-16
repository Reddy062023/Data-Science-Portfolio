# SQL Analytics — Multi-Domain Database Project

## Overview
Production-grade SQL project covering 4 business domains with 12 tables, sample data,
and 50+ queries demonstrating core to advanced SQL concepts using MySQL 8.0.

---

## Project Structure
```
SQL-Analytics/
├── queries/
│   ├── 01_basic_queries.sql       # SELECT, WHERE, ORDER BY, LIMIT
│   ├── 02_joins.sql               # INNER, LEFT, RIGHT, SELF JOIN
│   ├── 03_aggregations.sql        # GROUP BY, HAVING, COUNT, SUM, AVG
│   ├── 04_window_functions.sql    # RANK, DENSE_RANK, LAG, LEAD, OVER
│   ├── 05_subqueries_ctes.sql     # Subqueries, CTEs, nested queries
│   └── 06_stored_procedures.sql   # Stored procedures with IN/OUT params
└── README.md
```

---

## Database — `portfolio_analytics`

### 4 Domains — 12 Tables

**E-Commerce**
| Table | Description | Rows |
|-------|-------------|------|
| `customers` | Customer profiles with loyalty tier | 10 |
| `products` | Product catalog with pricing | 10 |
| `orders` | Customer orders with status | 15 |
| `order_items` | Line items per order | 23 |

**Healthcare**
| Table | Description | Rows |
|-------|-------------|------|
| `patients` | Patient demographics | 10 |
| `doctors` | Doctor profiles with specialization | 5 |
| `admissions` | Hospital admissions with cost | 15 |

**Finance**
| Table | Description | Rows |
|-------|-------------|------|
| `borrowers` | Borrower profiles with credit score | 10 |
| `loans` | Loan details with default status | 15 |

**HR**
| Table | Description | Rows |
|-------|-------------|------|
| `departments` | Company departments | 5 |
| `employees` | Employee profiles with salary | 15 |
| `salaries` | Salary history per employee | 10 |

---

## SQL Concepts Covered

### 01 — Basic Queries
- `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`
- Filtering by text, numbers, dates
- 15 queries across all 4 domains

### 02 — JOINs
- `INNER JOIN` — matching records only
- `LEFT JOIN` — all records including no match
- `SELF JOIN` — employees and their managers
- Multi-table joins (3+ tables)
- 10 queries across all 4 domains

### 03 — Aggregations
- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- `GROUP BY` with multiple columns
- `HAVING` to filter grouped results
- Monthly revenue trends
- 13 queries across all 4 domains

### 04 — Window Functions
- `RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`
- `LAG()`, `LEAD()` for time series
- `SUM() OVER`, `AVG() OVER`
- `PARTITION BY` for group-level calculations
- Running totals and month-over-month changes
- 10 queries across all 4 domains

### 05 — Subqueries & CTEs
- Subqueries in `WHERE`, `FROM`, `SELECT`
- Common Table Expressions (`WITH`)
- Multiple CTEs chained together
- `CROSS JOIN` with aggregation CTEs
- `CASE WHEN` for business segmentation
- 9 queries across all 4 domains

### 06 — Stored Procedures
- `IN` parameters for input
- `OUT` parameters for output
- `IF/ELSE` conditional logic
- `DECLARE` and variable assignment
- 5 procedures across all 4 domains

---

## Business Questions Answered

| Domain | Question |
|--------|---------|
| E-Commerce | Which customers are highest value? |
| E-Commerce | What is the monthly revenue trend? |
| E-Commerce | Which products are never ordered? |
| Healthcare | Which doctors generate most revenue? |
| Healthcare | Which patients have highest admission costs? |
| Healthcare | What is avg cost by insurance type? |
| Finance | What is default rate by loan grade? |
| Finance | Which borrowers are highest risk? |
| Finance | What is total exposure by loan purpose? |
| HR | Which departments pay above average? |
| HR | Who earns above their department average? |
| HR | What is the salary history per employee? |

---

## Setup & Usage

### 1. Connect to MySQL
```bash
mysql -u root -p
```

### 2. Create database and tables
```sql
CREATE DATABASE portfolio_analytics;
USE portfolio_analytics;
```

### 3. Run query files
```sql
SOURCE C:/Users/Geetu/DataScience/Data-Analysis-Portfolio/SQL-Analytics/queries/01_basic_queries.sql;
SOURCE C:/Users/Geetu/DataScience/Data-Analysis-Portfolio/SQL-Analytics/queries/02_joins.sql;
SOURCE C:/Users/Geetu/DataScience/Data-Analysis-Portfolio/SQL-Analytics/queries/03_aggregations.sql;
SOURCE C:/Users/Geetu/DataScience/Data-Analysis-Portfolio/SQL-Analytics/queries/04_window_functions.sql;
SOURCE C:/Users/Geetu/DataScience/Data-Analysis-Portfolio/SQL-Analytics/queries/05_subqueries_ctes.sql;
SOURCE C:/Users/Geetu/DataScience/Data-Analysis-Portfolio/SQL-Analytics/queries/06_stored_procedures.sql;
```

---

## Requirements
| Tool | Version |
|------|---------|
| MySQL | 8.0+ |
| MySQL Workbench | 8.0+ (optional) |

---

## Author
**Japendra**
Data Analysis Portfolio — SQL Analytics Project