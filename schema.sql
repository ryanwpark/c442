CREATE DATABASE budget_db;

USE budget_db;

 

CREATE TABLE user (

	user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,

    username VARCHAR(30) NOT NULL,

    email VARCHAR(50) NOT NULL,

    password_hash VARCHAR(100) NOT NULL

);

 

CREATE TABLE budget (

	budget_id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT,

    month_year VARCHAR(7) NOT NULL, -- Format: YYYY-MM

    income DECIMAL(9,2),

    FOREIGN KEY (user_id) REFERENCES user(user_id)

);

 

CREATE TABLE category (

	category_id INT PRIMARY KEY AUTO_INCREMENT,

    budget_id INT,

    cat_name VARCHAR(40) NOT NULL,

    allocated_income DECIMAL(9,2) NOT NULL,

    FOREIGN KEY (budget_id) REFERENCES budget(budget_id)

);

 

CREATE TABLE transactions (

    transaction_id INT AUTO_INCREMENT PRIMARY KEY,

    category_id INT NOT NULL,

    amount DECIMAL(10,2) NOT NULL,

    merchant_name VARCHAR(100),

    transaction_date DATE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (category_id) REFERENCES category(category_id)

);