import os
from flask import Flask, redirect, url_for
from view.dashboard_view import dashboard_blueprint

app = Flask(__name__)

app.register_blueprint(dashboard_blueprint)

@app.route('/')
def index():
    return redirect(url_for('dashboard.show_dashboard'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)