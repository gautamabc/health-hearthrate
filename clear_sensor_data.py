"""
Script to clear all sensor data from the database
"""
from app import app, db
from models import SensorData

def clear_all_sensor_data():
    """
    Remove all sensor data from the database
    """
    with app.app_context():
        # Delete all sensor data
        count = db.session.query(SensorData).delete()
        db.session.commit()
        print(f"Cleared {count} sensor readings from the database")

if __name__ == "__main__":
    clear_all_sensor_data()