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

    def get_user_by_username(self, username):
        sql = "SELECT * FROM user WHERE username = %s"
        self.cursor.execute(sql, (username,))
        return self.cursor.fetchone()

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

    #--- Expenses (Transactions) ---

    def get_user_expenses(self, user_id, month):
        sql = "SELECT Expense.ExpenseID AS transaction_id, Expense.Description AS name, Category.CategoryName AS category, Expense.AmountSpent AS cost, Expense.ExpenseDate AS date " \
              "FROM Expense JOIN Category ON Expense.CategoryID = Category.CategoryID " \
              "WHERE Expense.UserID = %s AND DATE_FORMAT(Expense.ExpenseDate, '%Y-%m') = %s " \
              "ORDER BY Expense.ExpenseDate DESC;"
        self.cursor.execute(sql, (user_id, month))
        return self.cursor.fetchall()

    def add_expense(self, user_id, name, category_name, cost, date):
        self.cursor.execute("SELECT CategoryID FROM Category WHERE UserID = %s AND CategoryName = %s LIMIT 1", (user_id, category_name))
        result = self.cursor.fetchone()
        if not result:
            return None
        cat_id = result["CategoryID"]
        sql = "INSERT INTO Expense (UserID, CategoryID, AmountSpent, Description, ExpenseDate) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (user_id, cat_id, cost, name, date))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_transaction(self, user_id, transaction_id, category_name, amount, merchant_name, transaction_date):
        self.cursor.execute("SELECT CategoryID FROM Category WHERE UserID = %s AND CategoryName = %s LIMIT 1", (user_id, category_name))
        result = self.cursor.fetchone()
        if not result:
            return 0
        cat_id = result["CategoryID"]
        sql = "UPDATE Expense SET CategoryID = %s, AmountSpent = %s, Description = %s, ExpenseDate = %s WHERE ExpenseID = %s AND UserID = %s"
        self.cursor.execute(sql, (cat_id, amount, merchant_name, transaction_date, transaction_id, user_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_transaction(self, user_id, transaction_id):
        sql = "DELETE FROM Expense WHERE ExpenseID = %s AND UserID = %s"
        self.cursor.execute(sql, (transaction_id, user_id))
        self.conn.commit()
        return self.cursor.rowcount
