from flask import Blueprint, render_template, request, redirect, url_for
from .db import db
from .models import Sensor

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin dashboard
@bp.route('/')
def dashboard():
    sensors = Sensor.query.all()
    return render_template('admin_dashboard.html', sensors=sensors)

# Add a new sensor
@bp.route('/add_sensor', methods=['POST'])
def add_sensor():
    name = request.form.get('name')
    if not name:
        return "Sensor name required", 400

    sensor = Sensor(name=name, moisture_level=50)
    db.session.add(sensor)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))
