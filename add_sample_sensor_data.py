"""
Script to add concise sample sensor data for DHT11, AD8232, and MPU6050 sensors
"""
import os
import sys
from datetime import datetime, timedelta
import random
from app import app, db
from models import SensorData

# Clear existing data
def clear_existing_data(user_id=1):
    with app.app_context():
        # Delete existing sensor data for this user
        db.session.query(SensorData).filter_by(user_id=user_id).delete()
        db.session.commit()
        print(f"Cleared existing sensor data for user {user_id}")

# Sample data for the specific sensors
SENSORS = [
    {
        "name": "temperature",
        "device_id": "esp32-dht11-01",
        "unit": "celsius",
        "min_value": 36.0,
        "max_value": 37.8,
        "sample_data": [36.5, 36.7, 36.4, 36.9, 37.1, 37.0, 36.8, 37.2, 36.6, 36.3]
    },
    {
        "name": "humidity",
        "device_id": "esp32-dht11-01",
        "unit": "percent",
        "min_value": 40.0,
        "max_value": 60.0,
        "sample_data": [45, 42, 48, 51, 49, 52, 47, 45, 50, 53]
    },
    {
        "name": "heart_rate",
        "device_id": "esp32-ad8232-01",
        "unit": "bpm",
        "min_value": 60,
        "max_value": 100,
        "sample_data": [72, 75, 68, 71, 74, 76, 73, 70, 72, 75]
    },
    {
        "name": "ecg",
        "device_id": "esp32-ad8232-01",
        "unit": "mv",
        "min_value": -1.5,
        "max_value": 1.5,
        "sample_data": [0.2, 0.8, 0.1, -0.3, 0.9, 0.3, -0.2, 0.7, 0.2, -0.1]
    },
    {
        "name": "acceleration",
        "device_id": "esp32-mpu6050-01",
        "unit": "g",
        "min_value": 0.05,
        "max_value": 2.0,
        "sample_data": [0.2, 0.5, 0.3, 0.8, 1.2, 0.7, 0.4, 0.9, 0.6, 0.3]
    }
]

def add_sample_data(user_id=1, days_back=10):
    """
    Add exactly 10 sample readings for each sensor type over the recent days
    """
    with app.app_context():
        # Clear any existing data
        clear_existing_data(user_id)
        
        total_added = 0
        current_time = datetime.now()
        
        for sensor in SENSORS:
            print(f"Adding data for {sensor['name']} from {sensor['device_id']}...")
            
            # Use predefined sample data
            for i, value in enumerate(sensor['sample_data']):
                # Calculate timestamp - most recent first
                days_ago = i  # 0 to 9 days ago
                reading_time = current_time - timedelta(days=days_ago)
                
                # Create the reading
                reading = SensorData(
                    user_id=user_id,
                    sensor_type=sensor['name'],
                    value=value,
                    unit=sensor['unit'],
                    device_id=sensor['device_id'],
                    timestamp=reading_time,
                    notes=f"Sample {sensor['name']} data from {days_ago} days ago"
                )
                
                db.session.add(reading)
                total_added += 1
            
        # Commit all readings at once
        db.session.commit()
        print(f"Added {total_added} sample sensor readings to the database")

if __name__ == "__main__":
    # Get user ID from command line if provided
    user_id = 1
    if len(sys.argv) > 1:
        try:
            user_id = int(sys.argv[1])
        except ValueError:
            print("Invalid user ID, using default (1)")
    
    add_sample_data(user_id=user_id)