"""
registration_view.py - The VIEW layer (MVC Pattern)

This file handles everything the USER SEES for registration:
  - Defines the web page routes (URLs)
  - Renders the HTML registration form
  - Sends user input to the Controller for processing

The View does NOT contain any business logic or database code.
It only:
  1. Shows the form (GET /register)
  2. Grabs what the user typed and passes it to the Controller (POST /register)
  3. Displays the result message back to the user
"""

from flask import Blueprint, request, render_template_string
from controller import register_user

view_blueprint = Blueprint("view", __name__)


# ──────────────────────────────────────────────
# HTML TEMPLATE (inline for simplicity)
# ──────────────────────────────────────────────

REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
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
        .register-card {
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
    </style>
</head>
<body>
    <div class="register-card">
        <h1>Create Account</h1>

        <!-- Show success or error message if there is one -->
        {% if message %}
            <div class="message {{ 'success' if success else 'error' }}">
                {{ message }}
            </div>
        {% endif %}

        <!-- Registration form -->
        <form method="POST" action="/register">
            <label for="username">Username</label>
            <input type="text" id="username" name="username"
                   placeholder="Enter a username" required>

            <label for="password">Password</label>
            <input type="password" id="password" name="password"
                   placeholder="Enter a password" required>

            <label for="verify_password">Verify Password</label>
            <input type="password" id="verify_password" name="verify_password"
                   placeholder="Re-enter your password" required>

            <button type="submit">Register</button>
        </form>
    </div>
</body>
</html>
"""


# ──────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────

@view_blueprint.route("/register", methods=["GET"])
def show_register_form():
    """
    GET /register
    Show the empty registration form.
    """
    return render_template_string(REGISTER_HTML, message=None, success=False)


@view_blueprint.route("/register", methods=["POST"])
def handle_register():
    """
    POST /register
    The user submitted the form. Our job in the View is:
      1. Grab the form data
      2. Pass it to the Controller
      3. Display whatever message the Controller sends back
    """
    # Step 1: Get the form data the user typed in
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    verify_password = request.form.get("verify_password", "")

    # Step 2: Send it to the controller (the controller does all the logic)
    result = register_user(username, password, verify_password)

    # Step 3: Show the form again with the success/error message
    return render_template_string(
        REGISTER_HTML,
        message=result["message"],
        success=result["success"]
    )
