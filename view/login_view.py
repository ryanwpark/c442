"""
login_view.py - The VIEW layer for Login (MVC Pattern)

This file handles everything the USER SEES for login:
  - Defines the web page routes (URLs)
  - Renders the HTML login form
  - Sends user input to the Controller for authentication

The View does NOT contain any business logic or database code.
It only:
  1. Shows the login form (GET /login)
  2. Grabs what the user typed and passes it to the Controller (POST /login)
  3. Displays the result message back to the user
"""

from flask import Blueprint, request, render_template_string, redirect
from controller import login_user

# Blueprint for login routes
login_blueprint = Blueprint("login", __name__)


# ──────────────────────────────────────────────
# HTML TEMPLATE (inline for simplicity)
# ──────────────────────────────────────────────

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        /* ── Page styling ── */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }

        /* ── Form card ── */
        .login-card {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }

        /* ── Form fields ── */
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }

        input:focus {
            outline: none;
            border-color: #4a90d9;
        }

        /* ── Submit button ── */
        button {
            width: 100%;
            padding: 12px;
            background-color: #4a90d9;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background-color: #357abd;
        }

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

        /* ── Register link ── */
        .register-link {
            text-align: center;
            margin-top: 15px;
            color: #555;
        }

        .register-link a {
            color: #4a90d9;
            text-decoration: none;
        }

        .register-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <h1>Login</h1>

        <!-- Show success or error message if there is one -->
        {% if message %}
            <div class="message {{ 'success' if success else 'error' }}">
                {{ message }}
            </div>
        {% endif %}

        <!-- Login form -->
        <form method="POST" action="/login">
            <label for="username">Username</label>
            <input type="text" id="username" name="username"
                   placeholder="Enter your username" required>

            <label for="password">Password</label>
            <input type="password" id="password" name="password"
                   placeholder="Enter your password" required>

            <button type="submit">Login</button>
        </form>

        <!-- Link to registration page -->
        <div class="register-link">
            Don't have an account? <a href="/register">Register here</a>
        </div>
    </div>
</body>
</html>
"""


# ──────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────

@login_blueprint.route("/login", methods=["GET"])
def show_login_form():
    """
    GET /login
    Show the empty login form.
    """
    return render_template_string(LOGIN_HTML, message=None, success=False)


@login_blueprint.route("/login", methods=["POST"])
def handle_login():
    """
    POST /login
    The user submitted the form. Our job in the View is:
      1. Grab the form data
      2. Pass it to the Controller
      3. Display whatever message the Controller sends back
    """
    # Step 1: Get the form data the user typed in
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Step 2: Send it to the controller
    result = login_user(username, password)

    # Step 3: If login succeeded, redirect to the home page
    if result["success"]:
        return redirect("/home")

    # If login failed, show the form again with the error message
    return render_template_string(
        LOGIN_HTML,
        message=result["message"],
        success=result["success"]
    )
