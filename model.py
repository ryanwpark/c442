import mysql.connector
from config import DB_CONFIG
from datetime import datetime

class BudgetModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    #--- Users ---


    def create_user(self, username, email, password_hash):
        sql = "INSERT INTO user (username, email, password_hash) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (username, email, password_hash))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id):
        sql ="SELECT * FROM user WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def get_all_users(self):
        sql = "SELECT * FROM user"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    #--- Budgets ---

    def create_budget(self, user_id, month_year, income):
        sql = "INSERT INTO budget (user_id, month_year, income) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (user_id, month_year, income))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_budget(self, budget_id):
        sql = "SELECT * FROM budget WHERE budget_id = %s"
        self.cursor.execute(sql, (budget_id,))
        return self.cursor.fetchone()

    def get_user_budgets(self, user_id):
        sql = "SELECT * FROM budget WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchall()

    #--- Categories ---

    def create_category(self, budget_id, cat_name, allocated_income):
        sql = "INSERT INTO category (budget_id, cat_name, allocated_income) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (budget_id, cat_name, allocated_income))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_category(self, category_id):
        sql = "SELECT * FROM category WHERE category_id = %s"
        self.cursor.execute(sql, (category_id,))
        return self.cursor.fetchone()

    def get_budget_categories(self, budget_id):
        sql = "SELECT * FROM category WHERE budget_id = %s"
        self.cursor.execute(sql, (budget_id,))
        return self.cursor.fetchall()

    #--- Transactions ---

    def get_user_expenses(self, user_id, month):
        sql = "SELECT u.username,t.transaction_id, t.merchant_name AS name, c.cat_name AS category, t.amount as cost, t.transaction_date AS date \
        FROM transactions t JOIN category c ON t.category_id = c.category_id \
        JOIN budget b ON c.budget_id = b.budget_id \
        JOIN user u ON b.user_id = u.user_id \
        WHERE u.user_id = %s AND b.month_year = %s \
        ORDER BY t.transaction_date DESC;"
        self.cursor.execute(sql, (user_id, month))
        expenses = self.cursor.fetchall()
        return expenses

    def add_expense(self, name, category_name, cost, date):
        self.cursor.execute("SELECT category_id FROM category WHERE cat_name = %s LIMIT 1", (category_name,))
        result = self.cursor.fetchone()
        cat_id = result["category_id"]
        sql = "INSERT INTO transactions (category_id, amount, merchant_name, transaction_date, created_at) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (cat_id, cost, name, date, datetime.today().strftime("%Y-%m-%d")))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_transaction(self, transaction_id, category_id, amount, merchant_name, transaction_date):
        sql = "UPDATE transactions SET category_id = %s, amount = %s, merchant_name = %s, transaction_date = %s WHERE transaction_id = %s"
        self.cursor.execute(sql, (category_id, amount, merchant_name, transaction_date, transaction_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_transaction(self, transaction_id):
        sql = "DELETE FROM transactions WHERE transaction_id = %s"
        self.cursor.execute(sql, (transaction_id,))
        self.conn.commit()
        return self.cursor.rowcount
