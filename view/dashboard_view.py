"""
dashboard_view.py - The VIEW layer for the Expense Dashboard (MVC Pattern)

This file handles everything the USER SEES for the expense dashboard:
  - Shows monthly, weekly, and daily expense summaries
  - Displays a list of all expenses
  - Provides a form to add new expenses
  - Allows editing and deleting expenses

The View does NOT contain any business logic or database code.
It only:
  1. Shows the dashboard page (GET /dashboard)
  2. Handles form submissions for add/edit/delete (POST routes)
  3. Passes user input to the Controller for processing
  4. Displays the results back to the user

TODO: Connect to Controller once expense controller functions are implemented.
"""

from flask import Blueprint, request, render_template_string, redirect, url_for
from datetime import datetime, timedelta

# Blueprint for dashboard routes
dashboard_blueprint = Blueprint("dashboard", __name__)


# ──────────────────────────────────────────────
# PLACEHOLDER DATA (until Controller/Model are connected)
# ──────────────────────────────────────────────

# In-memory list so we can demo add/edit/delete without a database
_sample_expenses = [
    {"id": 1, "name": "Grocery Run",       "category": "Food",          "cost": 52.30,  "date": "2026-03-23"},
    {"id": 2, "name": "Bus Pass",          "category": "Transport",     "cost": 25.00,  "date": "2026-03-22"},
    {"id": 3, "name": "Netflix",           "category": "Entertainment", "cost": 15.99,  "date": "2026-03-20"},
    {"id": 4, "name": "Electric Bill",     "category": "Utilities",     "cost": 87.50,  "date": "2026-03-18"},
    {"id": 5, "name": "Gym Membership",    "category": "Health",        "cost": 40.00,  "date": "2026-03-15"},
    {"id": 6, "name": "New Headphones",    "category": "Shopping",      "cost": 79.99,  "date": "2026-03-10"},
]
_next_id = 7

# Categories for the dropdown
CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Utilities",
    "Health",
    "Shopping",
    "Other",
]


# ──────────────────────────────────────────────
# HELPER FUNCTIONS (temporary, until Controller)
# ──────────────────────────────────────────────

def _get_all_expenses():
    """Return all expenses (placeholder)."""
    return list(_sample_expenses)


def _compute_summaries(expenses):
    """
    Compute monthly, weekly, and daily totals.
    Returns a dict with 'monthly', 'weekly', 'daily' totals.
    """
    today = datetime.today().date()
    start_of_month = today.replace(day=1)
    start_of_week = today - timedelta(days=today.weekday())  # Monday

    monthly_total = 0.0
    weekly_total = 0.0
    daily_total = 0.0

    for exp in expenses:
        exp_date = datetime.strptime(exp["date"], "%Y-%m-%d").date()
        if exp_date >= start_of_month:
            monthly_total += exp["cost"]
        if exp_date >= start_of_week:
            weekly_total += exp["cost"]
        if exp_date == today:
            daily_total += exp["cost"]

    return {
        "monthly": round(monthly_total, 2),
        "weekly": round(weekly_total, 2),
        "daily": round(daily_total, 2),
    }


# ──────────────────────────────────────────────
# HTML TEMPLATE (inline for simplicity)
# ──────────────────────────────────────────────

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expense Dashboard</title>
    <style>
        /* ── Reset & Base ── */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 20px;
        }

        /* ── Page Container ── */
        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }

        /* ── Summary Cards ── */
        .summary-row {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }

        .summary-card {
            flex: 1;
            background: white;
            padding: 25px 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .summary-card .label {
            font-size: 14px;
            color: #777;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .summary-card .amount {
            font-size: 28px;
            font-weight: bold;
            color: #333;
        }

        .summary-card.monthly .amount { color: #4a90d9; }
        .summary-card.weekly  .amount { color: #27ae60; }
        .summary-card.daily   .amount { color: #e67e22; }

        /* ── Add / Edit Expense Form ── */
        .form-card {
            background: white;
            padding: 25px 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }

        .form-card h2 {
            margin-bottom: 20px;
            color: #333;
            font-size: 20px;
        }

        .form-row {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: flex-end;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            flex: 1;
            min-width: 140px;
        }

        .form-group label {
            font-size: 13px;
            color: #555;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .form-group input,
        .form-group select {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #4a90d9;
        }

        .btn-add {
            padding: 10px 25px;
            background-color: #4a90d9;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
            align-self: flex-end;
            white-space: nowrap;
        }

        .btn-add:hover {
            background-color: #357abd;
        }

        /* ── Hidden edit ID field ── */
        .hidden { display: none; }

        /* ── Messages ── */
        .message {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
        }

        .message.success {
            background-color: #d4edda;
            color: #155724;
        }

        .message.error {
            background-color: #f8d7da;
            color: #721c24;
        }

        /* ── Expense Table ── */
        .table-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .table-card h2 {
            padding: 20px 25px 15px;
            color: #333;
            font-size: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        thead {
            background-color: #f8f9fa;
        }

        th {
            text-align: left;
            padding: 12px 20px;
            font-size: 13px;
            color: #777;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #eee;
        }

        td {
            padding: 14px 20px;
            font-size: 14px;
            border-bottom: 1px solid #f0f0f0;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover {
            background-color: #f9fbff;
        }

        .cost-cell {
            font-weight: bold;
            color: #e74c3c;
        }

        .category-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }

        .cat-food          { background-color: #e67e22; }
        .cat-transport      { background-color: #3498db; }
        .cat-entertainment  { background-color: #9b59b6; }
        .cat-utilities      { background-color: #1abc9c; }
        .cat-health         { background-color: #2ecc71; }
        .cat-shopping       { background-color: #e74c3c; }
        .cat-other          { background-color: #95a5a6; }

        /* ── Action Buttons ── */
        .actions {
            display: flex;
            gap: 8px;
        }

        .btn-edit {
            padding: 5px 12px;
            background-color: #f39c12;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
        }

        .btn-edit:hover {
            background-color: #d68910;
        }

        .btn-delete {
            padding: 5px 10px;
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            font-weight: bold;
        }

        .btn-delete:hover {
            background-color: #c0392b;
        }

        /* ── Empty state ── */
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #999;
            font-size: 15px;
        }

        /* ── Responsive ── */
        @media (max-width: 600px) {
            .summary-row { flex-direction: column; }
            .form-row { flex-direction: column; }
            th, td { padding: 10px 12px; font-size: 13px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Expense Dashboard</h1>

        <!-- ── Summary Cards ── -->
        <div class="summary-row">
            <div class="summary-card monthly">
                <div class="label">This Month</div>
                <div class="amount">${{ "%.2f"|format(summary.monthly) }}</div>
            </div>
            <div class="summary-card weekly">
                <div class="label">This Week</div>
                <div class="amount">${{ "%.2f"|format(summary.weekly) }}</div>
            </div>
            <div class="summary-card daily">
                <div class="label">Today</div>
                <div class="amount">${{ "%.2f"|format(summary.daily) }}</div>
            </div>
        </div>

        <!-- ── Messages ── -->
        {% if message %}
            <div class="message {{ 'success' if success else 'error' }}">
                {{ message }}
            </div>
        {% endif %}

        <!-- ── Add / Edit Expense Form ── -->
        <div class="form-card">
            <h2 id="form-title">Add Expense</h2>
            <form id="expense-form" method="POST" action="/dashboard/add">
                <input type="hidden" id="edit-id" name="edit_id" value="">
                <div class="form-row">
                    <div class="form-group">
                        <label for="name">Expense Name</label>
                        <input type="text" id="name" name="name"
                               placeholder="e.g. Grocery Run" required>
                    </div>

                    <div class="form-group">
                        <label for="category">Category</label>
                        <select id="category" name="category" required>
                            <option value="" disabled selected>Select...</option>
                            {% for cat in categories %}
                                <option value="{{ cat }}">{{ cat }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="cost">Cost ($)</label>
                        <input type="number" id="cost" name="cost"
                               step="0.01" min="0" placeholder="0.00" required>
                    </div>

                    <div class="form-group">
                        <label for="date">Date</label>
                        <input type="date" id="date" name="date"
                               value="{{ today }}" required>
                    </div>

                    <button type="submit" class="btn-add" id="submit-btn">Add</button>
                </div>
            </form>
        </div>

        <!-- ── Expense Table ── -->
        <div class="table-card">
            <h2>All Expenses</h2>
            {% if expenses %}
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Cost</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for exp in expenses %}
                    <tr>
                        <td>{{ exp.name }}</td>
                        <td>
                            <span class="category-badge cat-{{ exp.category|lower }}">
                                {{ exp.category }}
                            </span>
                        </td>
                        <td class="cost-cell">${{ "%.2f"|format(exp.cost) }}</td>
                        <td>{{ exp.date }}</td>
                        <td class="actions">
                            <button class="btn-edit"
                                    onclick="startEdit({{ exp.id }}, '{{ exp.name }}', '{{ exp.category }}', {{ exp.cost }}, '{{ exp.date }}')">
                                Edit
                            </button>
                            <form method="POST" action="/dashboard/delete/{{ exp.id }}"
                                  style="display:inline;"
                                  onsubmit="return confirm('Delete this expense?');">
                                <button type="submit" class="btn-delete">✕</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                No expenses yet. Add one above!
            </div>
            {% endif %}
        </div>
    </div>

    <!-- ── JavaScript for Edit Mode ── -->
    <script>
        function startEdit(id, name, category, cost, date) {
            // Update form title and button text
            document.getElementById('form-title').textContent = 'Edit Expense';
            document.getElementById('submit-btn').textContent = 'Save';

            // Fill the form fields
            document.getElementById('name').value = name;
            document.getElementById('category').value = category;
            document.getElementById('cost').value = cost;
            document.getElementById('date').value = date;

            // Point the form to the edit route
            document.getElementById('expense-form').action = '/dashboard/edit/' + id;
            document.getElementById('edit-id').value = id;

            // Scroll to the form
            document.getElementById('form-title').scrollIntoView({ behavior: 'smooth' });
        }
    </script>
</body>
</html>
"""


# ──────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────

@dashboard_blueprint.route("/dashboard", methods=["GET"])
def show_dashboard():
    """
    GET /dashboard
    Show the expense dashboard with summaries and expense list.
    """
    expenses = _get_all_expenses()
    summary = _compute_summaries(expenses)
    today = datetime.today().strftime("%Y-%m-%d")

    return render_template_string(
        DASHBOARD_HTML,
        expenses=expenses,
        summary=summary,
        categories=CATEGORIES,
        today=today,
        message=request.args.get("message"),
        success=request.args.get("success", "false") == "true",
    )


@dashboard_blueprint.route("/dashboard/add", methods=["POST"])
def add_expense():
    """
    POST /dashboard/add
    Add a new expense from the form.

    TODO: Replace with controller call once controller is implemented.
    """
    global _next_id

    name = request.form.get("name", "").strip()
    category = request.form.get("category", "")
    cost = request.form.get("cost", "0")
    date = request.form.get("date", "")

    # Basic validation (will move to controller later)
    if not name or not category or not date:
        return redirect(url_for("dashboard.show_dashboard",
                                message="All fields are required.",
                                success="false"))

    try:
        cost = round(float(cost), 2)
    except ValueError:
        return redirect(url_for("dashboard.show_dashboard",
                                message="Cost must be a valid number.",
                                success="false"))

    _sample_expenses.append({
        "id": _next_id,
        "name": name,
        "category": category,
        "cost": cost,
        "date": date,
    })
    _next_id += 1

    return redirect(url_for("dashboard.show_dashboard",
                            message="Expense added!",
                            success="true"))


@dashboard_blueprint.route("/dashboard/edit/<int:expense_id>", methods=["POST"])
def edit_expense(expense_id):
    """
    POST /dashboard/edit/<id>
    Update an existing expense.

    TODO: Replace with controller call once controller is implemented.
    """
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "")
    cost = request.form.get("cost", "0")
    date = request.form.get("date", "")

    if not name or not category or not date:
        return redirect(url_for("dashboard.show_dashboard",
                                message="All fields are required.",
                                success="false"))

    try:
        cost = round(float(cost), 2)
    except ValueError:
        return redirect(url_for("dashboard.show_dashboard",
                                message="Cost must be a valid number.",
                                success="false"))

    for exp in _sample_expenses:
        if exp["id"] == expense_id:
            exp["name"] = name
            exp["category"] = category
            exp["cost"] = cost
            exp["date"] = date
            return redirect(url_for("dashboard.show_dashboard",
                                    message="Expense updated!",
                                    success="true"))

    return redirect(url_for("dashboard.show_dashboard",
                            message="Expense not found.",
                            success="false"))


@dashboard_blueprint.route("/dashboard/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    """
    POST /dashboard/delete/<id>
    Delete an expense by its ID.

    TODO: Replace with controller call once controller is implemented.
    """
    global _sample_expenses
    original_len = len(_sample_expenses)
    _sample_expenses = [e for e in _sample_expenses if e["id"] != expense_id]

    if len(_sample_expenses) < original_len:
        return redirect(url_for("dashboard.show_dashboard",
                                message="Expense deleted.",
                                success="true"))

    return redirect(url_for("dashboard.show_dashboard",
                            message="Expense not found.",
                            success="false"))
