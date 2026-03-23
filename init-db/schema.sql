CREATE DATABASE IF NOT EXISTS budget_db;

USE budget_db;

 

CREATE TABLE IF NOT EXISTS user (

	user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,

    username VARCHAR(30) NOT NULL,

    email VARCHAR(50) NOT NULL,

    password_hash VARCHAR(100) NOT NULL

);

 

CREATE TABLE IF NOT EXISTS budget (

	budget_id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT,

    month_year VARCHAR(7) NOT NULL, -- Format: YYYY-MM

    income DECIMAL(9,2),

    FOREIGN KEY (user_id) REFERENCES user(user_id)

);

 

CREATE TABLE IF NOT EXISTS category (

	category_id INT PRIMARY KEY AUTO_INCREMENT,

    budget_id INT,

    cat_name VARCHAR(40) NOT NULL,

    allocated_income DECIMAL(9,2) NOT NULL,

    FOREIGN KEY (budget_id) REFERENCES budget(budget_id)

);

 

CREATE TABLE IF NOT EXISTS transactions (

    transaction_id INT AUTO_INCREMENT PRIMARY KEY,

    category_id INT NOT NULL,

    amount DECIMAL(10,2) NOT NULL,

    merchant_name VARCHAR(100),

    transaction_date DATE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (category_id) REFERENCES category(category_id)

);

-- 1. Create a Test User
INSERT IGNORE INTO user (user_id, username, email, password_hash)
VALUES (1, 'Ian Brown', 'ian@example.com', 'pbkdf2:sha256:250000$hashedpassword');

-- 2. Create a Budget for March 2026
INSERT IGNORE INTO budget (budget_id, user_id, month_year, income)
VALUES (1, 1, '2026-03', 5000.00);

-- 3. Create Categories linked to that Budget
INSERT IGNORE INTO category (category_id, budget_id, cat_name, allocated_income)
VALUES
(1, 1, 'Housing', 2000.00),
(2, 1, 'Food', 800.00),
(3, 1, 'Transport', 400.00),
(4, 1, 'Entertainment', 300.00);

-- 4. Add Sample Transactions
INSERT IGNORE INTO transactions (category_id, amount, merchant_name, transaction_date)
VALUES
(1, 2000.00, 'Rent', '2026-03-01'),
(2, 45.50, 'Trader Joe\'s', '2026-03-05'),
(2, 12.00, 'Green Lane Coffee', '2026-03-10'),
(3, 2.90, 'MTA OMNY', '2026-03-12'),
(4, 18.00, 'AMC Lincoln Square', '2026-03-15');