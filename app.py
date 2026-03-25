import os
from flask import Flask, redirect, url_for
from view.dashboard_view import dashboard_blueprint
from view.registration_view import view_blueprint as registration_blueprint
from view.login_view import login_blueprint
from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-key-only")
metrics = PrometheusMetrics(app, endpoint='/metrics')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Static information as metric
metrics.info('app_info', 'Budget App info', version='1.0.0')
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(registration_blueprint)

@app.route('/')
def index():
    return redirect(url_for('dashboard.show_dashboard'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=False)