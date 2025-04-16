"""
Script to add specific sensor data provided by the user
"""
from datetime import datetime, timedelta
from app import app, db
from models import SensorData

# Sample data directly from user's sensors
SENSOR_DATA = [
    # Format: (data_id, heart_rate, spo2, ecg, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, temp, humidity)
    (1, 72, 98, 0.9, 0.2, 0.1, 9.8, 0.1, -0.2, 0, 25.4, 55),
    (2, 80, 97, 1.1, 0.5, -0.3, 9.7, 0.2, -0.1, 0, 26.1, 53),
    (3, 65, 99, 0.8, -0.1, 0.2, 9.8, -0.1, 0, 0, 24.8, 57),
    (4, 90, 95, 1.4, 0.7, 0.5, 9.6, 0.3, -0.2, 0, 27.2, 50),
    (5, 75, 96, 1.0, 0, 0, 9.8, 0, 0, 0, 25.9, 52),
    (6, 68, 98, 0.7, -0.3, 0.1, 9.9, -0.1, 0, 0, 24.5, 58),
    (7, 110, 92, 1.8, 1.2, 0.8, 9.5, 0.5, -0.3, 0, 28.0, 48),
    (8, 60, 99, 0.6, -0.5, 0, 9.8, -0.2, 0, 0, 23.9, 60),
    (9, 85, 94, 1.2, 0.4, -0.2, 9.7, 0.2, -0.1, 0, 26.7, 51),
    (10, 78, 97, 1.0, 0.3, 0.1, 9.8, 0.1, 0, 0, 25.6, 54)
]

def add_sensor_data(user_id=1):
    """
    Add the specific sensor data points provided by the user
    """
    with app.app_context():
        # Clear existing sensor data
        db.session.query(SensorData).filter_by(user_id=user_id).delete()
        db.session.commit()
        print(f"Cleared existing sensor data for user {user_id}")
        
        # Current time to base timestamps on
        current_time = datetime.now()
        total_added = 0
        
        # Add data for each sensor type
        for idx, data in enumerate(SENSOR_DATA):
            (data_id, heart_rate, spo2, ecg, accel_x, accel_y, accel_z, 
             gyro_x, gyro_y, gyro_z, temp, humidity) = data
            
            # Calculate timestamp (newer data has more recent timestamp)
            reading_time = current_time - timedelta(days=len(SENSOR_DATA) - idx - 1)
            
            # Add heart rate data (from MAX30102)
            heart_reading = SensorData(
                user_id=user_id,
                sensor_type="heart_rate",
                value=heart_rate,
                unit="bpm",
                device_id="esp32-max30102-01",
                timestamp=reading_time,
                notes=f"Heart rate reading #{data_id}"
            )
            db.session.add(heart_reading)
            
            # Add SpO2 data (from MAX30102)
            spo2_reading = SensorData(
                user_id=user_id,
                sensor_type="blood_oxygen",
                value=spo2,
                unit="percent",
                device_id="esp32-max30102-01",
                timestamp=reading_time,
                notes=f"Blood oxygen reading #{data_id}"
            )
            db.session.add(spo2_reading)
            
            # Add ECG data (from AD8232)
            ecg_reading = SensorData(
                user_id=user_id,
                sensor_type="ecg",
                value=ecg,
                unit="mv",
                device_id="esp32-ad8232-01",
                timestamp=reading_time,
                notes=f"ECG reading #{data_id}"
            )
            db.session.add(ecg_reading)
            
            # Add acceleration data (from MPU6050)
            accel_reading = SensorData(
                user_id=user_id,
                sensor_type="acceleration",
                value=round((accel_x**2 + accel_y**2 + accel_z**2)**0.5, 2),  # Magnitude
                unit="g",
                device_id="esp32-mpu6050-01",
                timestamp=reading_time,
                notes=f"Acceleration reading #{data_id}: ({accel_x}, {accel_y}, {accel_z})"
            )
            db.session.add(accel_reading)
            
            # Add temperature data (from DHT11)
            temp_reading = SensorData(
                user_id=user_id,
                sensor_type="temperature",
                value=temp,
                unit="celsius",
                device_id="esp32-dht11-01",
                timestamp=reading_time,
                notes=f"Temperature reading #{data_id}"
            )
            db.session.add(temp_reading)
            
            # Add humidity data (from DHT11)
            humidity_reading = SensorData(
                user_id=user_id,
                sensor_type="humidity",
                value=humidity,
                unit="percent",
                device_id="esp32-dht11-01",
                timestamp=reading_time,
                notes=f"Humidity reading #{data_id}"
            )
            db.session.add(humidity_reading)
            
            total_added += 6  # 6 readings per data point
            
        # Commit all readings at once
        db.session.commit()
        print(f"Added {total_added} sensor readings to the database")

if __name__ == "__main__":
    add_sensor_data()