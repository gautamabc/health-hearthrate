"""
Script to add the specific sensor data table provided by the user
"""
from datetime import datetime, timedelta
from app import app, db
from models import SensorData

# Sample data directly from user's table:
# | Data ID | Heart Rate (BPM) | SpO₂ (%) | ECG (mV) | Acceleration (m/s²) | Gyro (°/s) | Temperature (°C) | Humidity (%) |
# |---------|----------------|---------|----------|-----------------|-----------|----------------|-------------|
# | 1       | 72             | 98      | 0.9      | (0.2, 0.1, 9.8) | (0.1, -0.2, 0) | 25.4           | 55          |
# | 2       | 80             | 97      | 1.1      | (0.5, -0.3, 9.7) | (0.2, -0.1, 0) | 26.1           | 53          |
# | 3       | 65             | 99      | 0.8      | (-0.1, 0.2, 9.8) | (-0.1, 0, 0) | 24.8           | 57          |
# | 4       | 90             | 95      | 1.4      | (0.7, 0.5, 9.6) | (0.3, -0.2, 0) | 27.2           | 50          |
# | 5       | 75             | 96      | 1.0      | (0, 0, 9.8) | (0, 0, 0) | 25.9           | 52          |
# | 6       | 68             | 98      | 0.7      | (-0.3, 0.1, 9.9) | (-0.1, 0, 0) | 24.5           | 58          |
# | 7       | 110            | 92      | 1.8      | (1.2, 0.8, 9.5) | (0.5, -0.3, 0) | 28.0           | 48          |
# | 8       | 60             | 99      | 0.6      | (-0.5, 0, 9.8) | (-0.2, 0, 0) | 23.9           | 60          |
# | 9       | 85             | 94      | 1.2      | (0.4, -0.2, 9.7) | (0.2, -0.1, 0) | 26.7           | 51          |
# | 10      | 78             | 97      | 1.0      | (0.3, 0.1, 9.8) | (0.1, 0, 0) | 25.6           | 54          |

TABLE_DATA = [
    # Format: data_id, heart_rate, spo2, ecg, accel, gyro, temp, humidity
    (1, 72, 98, 0.9, "(0.2, 0.1, 9.8)", "(0.1, -0.2, 0)", 25.4, 55),
    (2, 80, 97, 1.1, "(0.5, -0.3, 9.7)", "(0.2, -0.1, 0)", 26.1, 53),
    (3, 65, 99, 0.8, "(-0.1, 0.2, 9.8)", "(-0.1, 0, 0)", 24.8, 57),
    (4, 90, 95, 1.4, "(0.7, 0.5, 9.6)", "(0.3, -0.2, 0)", 27.2, 50),
    (5, 75, 96, 1.0, "(0, 0, 9.8)", "(0, 0, 0)", 25.9, 52),
    (6, 68, 98, 0.7, "(-0.3, 0.1, 9.9)", "(-0.1, 0, 0)", 24.5, 58),
    (7, 110, 92, 1.8, "(1.2, 0.8, 9.5)", "(0.5, -0.3, 0)", 28.0, 48),
    (8, 60, 99, 0.6, "(-0.5, 0, 9.8)", "(-0.2, 0, 0)", 23.9, 60),
    (9, 85, 94, 1.2, "(0.4, -0.2, 9.7)", "(0.2, -0.1, 0)", 26.7, 51),
    (10, 78, 97, 1.0, "(0.3, 0.1, 9.8)", "(0.1, 0, 0)", 25.6, 54)
]

def clear_sensor_data(user_id=1):
    """Clear all existing sensor data"""
    with app.app_context():
        count = db.session.query(SensorData).filter_by(user_id=user_id).delete()
        db.session.commit()
        print(f"Cleared {count} sensor readings from the database")

def add_table_data(user_id=1):
    """Add data from the table to the database"""
    with app.app_context():
        # Clear existing data
        clear_sensor_data(user_id)
        
        # Set start time (10 days ago)
        base_time = datetime.now() - timedelta(days=10)
        total_added = 0
        
        # Add each row of data
        for row in TABLE_DATA:
            data_id, heart_rate, spo2, ecg, accel, gyro, temp, humidity = row
            
            # Calculate timestamp
            timestamp = base_time + timedelta(days=data_id)
            
            # Add heart rate reading
            hr_reading = SensorData(
                user_id=user_id,
                sensor_type="heart_rate",
                value=heart_rate,
                unit="bpm",
                device_id="esp32-max30102-01",
                timestamp=timestamp,
                notes=f"Heart rate reading #{data_id}"
            )
            db.session.add(hr_reading)
            
            # Add SpO2 reading
            spo2_reading = SensorData(
                user_id=user_id,
                sensor_type="blood_oxygen",
                value=spo2,
                unit="percent",
                device_id="esp32-max30102-01",
                timestamp=timestamp,
                notes=f"Blood oxygen reading #{data_id}"
            )
            db.session.add(spo2_reading)
            
            # Add ECG reading
            ecg_reading = SensorData(
                user_id=user_id,
                sensor_type="ecg",
                value=ecg,
                unit="mv",
                device_id="esp32-ad8232-01",
                timestamp=timestamp,
                notes=f"ECG reading #{data_id}"
            )
            db.session.add(ecg_reading)
            
            # Add acceleration reading - use magnitude for the value
            accel_reading = SensorData(
                user_id=user_id,
                sensor_type="acceleration",
                value=9.8,  # Approximate magnitude
                unit="g",
                device_id="esp32-mpu6050-01",
                timestamp=timestamp,
                notes=f"Acceleration reading #{data_id}: {accel}"
            )
            db.session.add(accel_reading)
            
            # Add temperature reading
            temp_reading = SensorData(
                user_id=user_id,
                sensor_type="temperature",
                value=temp,
                unit="celsius",
                device_id="esp32-dht11-01",
                timestamp=timestamp,
                notes=f"Temperature reading #{data_id}"
            )
            db.session.add(temp_reading)
            
            # Add humidity reading
            humidity_reading = SensorData(
                user_id=user_id,
                sensor_type="humidity",
                value=humidity,
                unit="percent",
                device_id="esp32-dht11-01",
                timestamp=timestamp,
                notes=f"Humidity reading #{data_id}"
            )
            db.session.add(humidity_reading)
            
            total_added += 6
            
        # Commit all changes
        db.session.commit()
        print(f"Added {total_added} sensor readings from the table data")

if __name__ == "__main__":
    add_table_data()