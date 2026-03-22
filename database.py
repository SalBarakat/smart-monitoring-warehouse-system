import sqlite3
import paho.mqtt.client as mqtt
import json

import os
print(f"REAL DATABASE LOCATION: {os.path.abspath('warehouse.db')}")

#Database setup
def init_db():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_readings (id INTEGER PRIMARY KEY AUTOINCREMENT, temperature REAL, humidity REAL, vibration REAL, battery REAL, pallet_present BOOLEAN, timestamp TEXT, temperature_failed BOOLEAN DEFAULT FALSE, humidity_failed BOOLEAN DEFAULT FALSE, vibration_failed BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
             ''')
    conn.commit()
    return conn

#MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("warehouse/sensors")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print("New message arrived")
    try: 
        data = json.loads(msg.payload)
        print(f"Received data: {data}")
        conn = sqlite3.connect('warehouse.db')
        cursor = conn.cursor()
        cursor.execute('''Insert into sensor_readings (temperature, humidity, vibration, battery, pallet_present, timestamp) VALUES (?, ?, ?, ?, ?, ?)''', 
                    (data['temperature'], data['humidity'], data['vibration'], data['battery'], data['pallet_present'], data['timestamp']))
        conn.commit()
        conn.close()
        print("Data inserted into database successfully.")
    except Exception as e:
        print(f"Error processing message: {e}")





init_db()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever() 
