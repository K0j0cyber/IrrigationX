from flask import Blueprint, jsonify, request
from .db import db
from .models import Sensor, SensorLog

bp = Blueprint('api', __name__, url_prefix='/api')

# Get all sensors
@bp.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'moisture_level': s.moisture_level
    } for s in sensors])

# Update sensor moisture (called by simulator)
@bp.route('/sensors/<int:sensor_id>/moisture', methods=['POST'])
def update_moisture(sensor_id):
    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return jsonify({'error': 'Sensor not found'}), 404

    data = request.json
    sensor.moisture_level = data.get('moisture_level', sensor.moisture_level)
    db.session.commit()

    # Log the update
    log = SensorLog(sensor_id=sensor.id, moisture_level=sensor.moisture_level)
    db.session.add(log)
    db.session.commit()

    return jsonify({'message': f'Sensor {sensor.id} updated', 'moisture_level': sensor.moisture_level})

# Trigger irrigation for a sensor
@bp.route('/sensors/<int:sensor_id>/irrigate', methods=['POST'])
def irrigate_sensor(sensor_id):
    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return jsonify({'error': 'Sensor not found'}), 404

    # Example: simple irrigation logic
    if sensor.moisture_level < 50:
        sensor.moisture_level += 20
        db.session.commit()
        log = SensorLog(sensor_id=sensor.id, moisture_level=sensor.moisture_level)
        db.session.add(log)
        db.session.commit()
        return jsonify({'message': f'Sensor {sensor.id} irrigated', 'new_moisture': sensor.moisture_level})
    else:
        return jsonify({'message': f'Sensor {sensor.id} does not need irrigation', 'moisture': sensor.moisture_level})
