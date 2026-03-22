import datetime
import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'warehouse.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SensorData(db.Model):
    __tablename__ = 'sensor_readings'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    vibration = db.Column(db.Float)
    battery = db.Column(db.Float)
    pallet_present = db.Column(db.Boolean)
    timestamp = db.Column(db.String(100))
    temperature_failed = db.Column(db.Boolean, default=False)
    humidity_failed = db.Column(db.Boolean, default=False)
    vibration_failed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


@app.route('/', methods=['GET'])
def index():
    latest_readings = SensorData.query.order_by(SensorData.id.desc()).limit(15).all()
    return render_template('index.html', readings=latest_readings)


@app.route('/debug')
def debug():
    count = SensorData.query.count()
    latest = SensorData.query.order_by(SensorData.id.desc()).first()
    return jsonify({
        'total_rows': count,
        'latest_row': str(latest.__dict__) if latest else None
    })


@app.route('/api/sensor-data', methods=['POST'])
def get_latest_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    try:
        new_reading = SensorData(
            temperature=data['temperature'],
            humidity=data['humidity'],
            vibration=data['vibration'],
            battery=data['battery'],
            pallet_present=data['pallet_present'],
            timestamp=data['timestamp']
        )
        db.session.add(new_reading)
        db.session.commit()
        return jsonify({'message': 'Sensor data stored successfully'}), 201
    except Exception as e:
        print(f"Error saving sensor data: {e}")
        return jsonify({'error': 'Failed to save sensor data'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created")
    print(f"Flask is using database at: {os.path.abspath('warehouse.db')}")
    app.run(debug=True)