A real-time IoT sensor monitoring system that simulates warehouse sensors, transmits data via MQTT, stores it in a database, and displays it on a live web dashboard.

Overview:
This project simulates a smart warehouse environment where sensors track temperature, humidity, vibration, battery levels, and pallet presence. Data flows through an MQTT broker into a SQLite database and is visualized on a Flask web dashboard that auto-refreshes every 5 seconds.

Architecture:
Sensor Simulator → MQTT Broker → MQTT Subscriber → SQLite Database → Flask Dashboard

Technologies Used:
Python — core language
Paho MQTT — sensor data transmission
SQLite — lightweight database storage
Flask & SQLAlchemy — web server and ORM
HTML/CSS — dashboard frontend
Mosquitto — MQTT broker

How to Run:
Start Mosquitto MQTT broker,
Run the MQTT subscriber: python database.py,
Run the sensor simulator: python sensor_warehouse.py,
Run the Flask app: python app.py,
Open http://127.0.0.1:5000 in your browser

Features:
1-Real-time sensor data simulation (temperature, humidity, vibration)
 2-Random sensor failure simulation (5% chance per reading)
 3-Battery level monitoring with visual indicators
 4-Pallet presence detection
 5-Auto-refreshing web dashboard showing latest 15 readings
 6-Data persistence with SQLite

 You can find a concise step by step guide for this project in the file "smart warehouse monitoring system.pdf"


 
