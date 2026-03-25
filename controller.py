from model import BudgetModel
import hashlib

model = BudgetModel()

# --- Auth ---

def register_user(username, password, verify_password):
    if not username or not password:
        return {"success": False, "message": "Username and password are required."}
    if password != verify_password:
        return {"success": False, "message": "Passwords do not match."}
    existing = model.get_user_by_username(username)
    if existing:
        return {"success": False, "message": "Username already taken."}
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    model.create_user(username, username + "@email.com", password_hash)
    return {"success": True, "message": "Account created!"}

def login_user(username, password):
    if not username or not password:
        return {"success": False, "message": "Username and password are required."}
    user = model.get_user_by_username(username)
    if not user:
        return {"success": False, "message": "User not found."}
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user["password_hash"] != password_hash:
        return {"success": False, "message": "Wrong password."}
    return {"success": True, "message": "Login successful.", "user_id": user["user_id"]}

# --- Users ---

def create_user(username, email, password_hash):
    return model.create_user(username, email, password_hash)

def get_user(user_id):
    return model.get_user(user_id)

def get_all_users():
    return model.get_all_users()

# --- Budgets ---

def create_budget(user_id, month_year, income):
    return model.create_budget(user_id, month_year, income)

def get_budget(budget_id):
    return model.get_budget(budget_id)

def get_user_budgets(user_id):
    return model.get_user_budgets(user_id)

# --- Categories ---

def create_category(budget_id, cat_name, allocated_income):
    return model.create_category(budget_id, cat_name, allocated_income)

def get_category(category_id):
    return model.get_category(category_id)

def get_budget_categories(budget_id):
    return model.get_budget_categories(budget_id)

# --- Transactions ---

def get_user_expenses(user_id, month_year):
    return model.get_user_expenses(user_id, month_year)

def add_expense(name, category_name, cost, date):
    return model.add_expense(name, category_name, cost, date)

def update_transaction(transaction_id, category_id, amount, merchant_name, date):
    return model.update_transaction(transaction_id, category_id, amount, merchant_name, date)

def delete_transaction(transaction_id):
    return model.delete_transaction(transaction_id)
