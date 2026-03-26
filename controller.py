from model import BudgetModel
from prometheus_client import Counter, Gauge
import hashlib

model = BudgetModel()

# Track every time a transaction is added
TRANSACTION_COUNT = Counter('budget_transactions_total', 'Total expenses logged')
# Track the total dollar amount spent (Gauge)
TOTAL_SPENT = Gauge('budget_dollars_spent_total', 'Total cumulative spending across all users')
FAILED_LOGINS = Counter('budget_login_failures_total', 'Number of failed login attempts')
# Track unique logins
USER_LOGIN_TRACKER = Counter('budget_user_login_total', 'Logins tracked by user ID', ['user_id'])
# Track login attempts
LOGIN_ATTEMPTS = Counter('budget_login_attempts_total', 'Total login attempts (success + failure)', ['result'])
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
    user_id = model.create_user(username, username + "@email.com", password_hash)

    set_user_defaults(user_id)
    return {"success": True, "message": "Account created!"}

def login_user(username, password):
    if not username or not password:
        return {"success": False, "message": "Username and password are required."}
    user = model.get_user_by_username(username)
    if not user:
        FAILED_LOGINS.inc()
        LOGIN_ATTEMPTS.labels(result='failure').inc()
        return {"success": False, "message": "User not found."}
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user["password_hash"] != password_hash:
        FAILED_LOGINS.inc()
        LOGIN_ATTEMPTS.labels(result='failure').inc()
        return {"success": False, "message": "Wrong password."}

    # Track successful logins
    LOGIN_ATTEMPTS.labels(result='success').inc()  # Label for percentage
    USER_LOGIN_TRACKER.labels(user_id=user["user_id"]).inc()  # Track THIS specific user

    return {"success": True, "message": "Login successful.", "user_id": user["user_id"]}

# --- Users ---

def create_user(username, email, password_hash):
    return model.create_user(username, email, password_hash)


def set_user_defaults(user_id):
    # Creates a default budget for the current month
    from datetime import datetime
    current_month = datetime.today().strftime("%Y-%m-%d")[:7]  # e.g., "2026-03"

    # 1. Create the budget record (default income: 0.00)
    budget_id = model.create_budget(user_id, current_month, 0.00)

    # 2. Create default categories linked to this budget
    default_categories = ["Housing", "Food", "Transport", "Entertainment", "Utilities", "Health", "Shopping", "Other"]
    for cat in default_categories:
        model.create_category(budget_id, cat, 0.00)

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

def add_expense(user_id, name, category_name, cost, date):
    result = model.add_expense(user_id, name, category_name, cost, date)
    # Increment metrics if the DB insert was successful
    if result:
        TRANSACTION_COUNT.inc()
        try:
            TOTAL_SPENT.inc(float(cost))
        except (ValueError, TypeError):
            pass

    return result

def update_transaction(user_id, transaction_id, category_id, amount, merchant_name, date):
    return model.update_transaction(user_id, transaction_id, category_id, amount, merchant_name, date)

def delete_transaction(user_id, transaction_id):
    return model.delete_transaction(user_id, transaction_id)
