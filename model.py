import mysql.connector
from config import DB_CONFIG
from datetime import datetime

class BudgetModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

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
        cat_id = self.cursor.fetchone()[0]
        sql = "INSERT INTO transactions (category_id, amount, merchant_name, transaction_date, created_at) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (cat_id, cost, name, date, datetime.today().strftime("%Y-%m-%d")))
        self.conn.commit()
        return self.cursor.lastrowid


