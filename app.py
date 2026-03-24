import os
from flask import Flask, redirect, url_for
from view.dashboard_view import dashboard_blueprint
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, endpoint='/metrics')

# Static information as metric
metrics.info('app_info', 'Budget App info', version='1.0.0')
app.register_blueprint(dashboard_blueprint)

@app.route('/')
def index():
    return redirect(url_for('dashboard.show_dashboard'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=False)