from model import BudgetModel
from flask import jsonify
from prometheus_client import Counter

model = BudgetModel()

def get_dashboard_data(user_id, month_year):
    # Get raw data from model
    expenses = model.get_user_expenses(user_id, month_year)
    return expenses


