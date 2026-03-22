import json
import random
import time 
from datetime import datetime
import paho.mqtt.client as mqtt

# MQTT setup
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "warehouse/sensors"

# Function to check whether the MQTT broker is available
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

#Function to handle MQTT disconnection
def on_disconnect(client, userdata, rc):
    if rc !=0:
        print(f"Disconnected from MQTT Broker with return code {rc}")

# Message is successfully published callback
def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully.")

# Function to save sensor data to database
def save_to_database(data):
    print(f"Saving data to database: {data}")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

# Connect to broker
print("Connecting to MQTT broker...")
client.connect(mqtt_broker, mqtt_port, keepalive = 60)
client.loop_start()



# initial sensor values
temperature = 23.0
humidity = 50.0
vibration = 0.0
battery = 100.0
pallet_present = True
def simulate_Sensor_Data():
    global temperature, humidity, vibration, battery, pallet_present
    while True:
        # Simulate sensor data changes
        temperature += random.uniform(-0.5, 0.5)
        humidity += random.uniform(-1.0, 1.0)
        vibration = random.uniform(0.0, 1.0)
        battery -= random.uniform(0.1, 0.5)
        
        # put values in a reasonable range
        temperature = max(min(temperature, 30.0), 15.0)
        humidity = max(min(humidity, 80.0), 20.0)
        vibration = max(min(vibration, 1.0), 0.0)
        battery = max(battery, 0.0)

        if random.random() < 0.1:  # 10% chance of pallet being removed
            pallet_present = False
            print("Pallet removed from sensor area.")


        #lowering the battery level to simulate the need for charging
        if battery < 20.0:
            pallet_present = False
            print("Warning: Battery low! Pallet removed for charging.")
        else:
            pallet_present = True


        # Create a data dictionary
        data = {
            "timestamp": datetime.now().isoformat(),
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "vibration": round(vibration, 2),
            "battery": round(battery, 2),
            "pallet_present": pallet_present
        }

        #simulating random sensor failure
        for sensor in ["temperature", "humidity", "vibration"]:
            if random.random() < 0.05:  # 5% chance of failure 
                data[sensor] = None  # Simulate temperature sensor failure
                print(f"Warning: {sensor} sensor failure detected!")

        
        # Convert to JSON and print
        json_data = json.dumps(data)
        print(json_data)


        save_to_database(data)

        #Publish to MQTT broker
        if mqtt_topic:
            client.publish(mqtt_topic,json_data)

        # Wait for a few seconds before the next reading
        time.sleep(5)

try: 
    simulate_Sensor_Data()
except KeyboardInterrupt:
    print("/n Shutting down....")
    client.loop_stop()
    client.disconnect()




