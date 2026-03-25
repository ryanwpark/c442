from model import BudgetModel

model = BudgetModel()

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
