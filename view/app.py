import os
from flask import Flask, redirect, url_for
from dashboard_view import dashboard_blueprint

app = Flask(__name__)

app.register_blueprint(dashboard_blueprint)

@app.route('/')
def index():
    return redirect(url_for('dashboard.show_dashboard'))

if __name__ == "__main__":
    app.run(debug=True)