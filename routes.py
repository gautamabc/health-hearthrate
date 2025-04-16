from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_socketio import emit
from datetime import datetime, date
import json

from app import db, socketio
from models import User, Medication, DietEntry, Appointment, WaterIntake, CalorieEntry, SensorData
from forms import (LoginForm, RegistrationForm, ProfileForm, MedicationForm, DietEntryForm,
                 AppointmentForm, WaterIntakeForm, CalorieEntryForm, SymptomCheckerForm, SensorDataForm)
from helpers import load_health_articles, load_symptom_data, get_symptom_recommendations

def register_routes(app):
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            # For dashboard display
            today = date.today()
            medications = Medication.query.filter_by(user_id=current_user.id).all()
            today_medications = [med for med in medications if med.start_date <= today and (med.end_date is None or med.end_date >= today)]
            
            today_appointments = Appointment.query.filter_by(
                user_id=current_user.id, date=today).all()
            
            today_water = WaterIntake.query.filter_by(
                user_id=current_user.id, date=today).all()
            total_water = sum(intake.amount for intake in today_water)
            
            # Get diet entries for today
            today_diet = DietEntry.query.filter_by(
                user_id=current_user.id, date=today).all()
            total_calories = sum(entry.calories or 0 for entry in today_diet)
            
            return render_template('index.html', 
                                today_medications=today_medications,
                                today_appointments=today_appointments,
                                total_water=total_water,
                                total_calories=total_calories)
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm()
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.date_of_birth = form.date_of_birth.data
            current_user.gender = form.gender.data
            current_user.height = form.height.data
            current_user.weight = form.weight.data
            current_user.blood_type = form.blood_type.data
            current_user.allergies = form.allergies.data
            current_user.medical_conditions = form.medical_conditions.data
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.date_of_birth.data = current_user.date_of_birth
            form.gender.data = current_user.gender
            form.height.data = current_user.height
            form.weight.data = current_user.weight
            form.blood_type.data = current_user.blood_type
            form.allergies.data = current_user.allergies
            form.medical_conditions.data = current_user.medical_conditions
        return render_template('profile.html', form=form)
    
    @app.route('/medications', methods=['GET', 'POST'])
    @login_required
    def medications():
        form = MedicationForm()
        if form.validate_on_submit():
            medication = Medication(
                user_id=current_user.id,
                name=form.name.data,
                dosage=form.dosage.data,
                frequency=form.frequency.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                time_of_day=form.time_of_day.data,
                notes=form.notes.data
            )
            db.session.add(medication)
            db.session.commit()
            flash('Medication added successfully!', 'success')
            return redirect(url_for('medications'))
        
        medications_list = Medication.query.filter_by(user_id=current_user.id).all()
        today = date.today()
        return render_template('medications.html', form=form, medications=medications_list, today=today)
    
    @app.route('/medications/delete/<int:id>', methods=['POST'])
    @login_required
    def delete_medication(id):
        medication = Medication.query.get_or_404(id)
        if medication.user_id != current_user.id:
            flash('You are not authorized to delete this medication.', 'danger')
            return redirect(url_for('medications'))
        
        db.session.delete(medication)
        db.session.commit()
        flash('Medication deleted successfully!', 'success')
        return redirect(url_for('medications'))
    
    @app.route('/diet', methods=['GET', 'POST'])
    @login_required
    def diet():
        form = DietEntryForm()
        if form.validate_on_submit():
            diet_entry = DietEntry(
                user_id=current_user.id,
                meal_type=form.meal_type.data,
                food_items=form.food_items.data,
                calories=form.calories.data,
                protein=form.protein.data,
                carbs=form.carbs.data,
                fat=form.fat.data,
                date=form.date.data
            )
            db.session.add(diet_entry)
            db.session.commit()
            flash('Diet entry added successfully!', 'success')
            return redirect(url_for('diet'))
        
        # Default to today's date
        if request.method == 'GET':
            form.date.data = date.today()
        
        # Get today's diet entries
        today_entries = DietEntry.query.filter_by(
            user_id=current_user.id, 
            date=date.today()
        ).order_by(DietEntry.meal_type).all()
        
        # Calculate totals
        total_calories = sum(entry.calories or 0 for entry in today_entries)
        total_protein = sum(entry.protein or 0 for entry in today_entries)
        total_carbs = sum(entry.carbs or 0 for entry in today_entries)
        total_fat = sum(entry.fat or 0 for entry in today_entries)
        
        return render_template('diet.html', 
                            form=form, 
                            diet_entries=today_entries,
                            total_calories=total_calories,
                            total_protein=total_protein,
                            total_carbs=total_carbs,
                            total_fat=total_fat)
    
    @app.route('/diet/delete/<int:id>', methods=['POST'])
    @login_required
    def delete_diet_entry(id):
        diet_entry = DietEntry.query.get_or_404(id)
        if diet_entry.user_id != current_user.id:
            flash('You are not authorized to delete this entry.', 'danger')
            return redirect(url_for('diet'))
        
        db.session.delete(diet_entry)
        db.session.commit()
        flash('Diet entry deleted successfully!', 'success')
        return redirect(url_for('diet'))
    
    @app.route('/calendar', methods=['GET', 'POST'])
    @login_required
    def calendar():
        form = AppointmentForm()
        if form.validate_on_submit():
            appointment = Appointment(
                user_id=current_user.id,
                title=form.title.data,
                doctor=form.doctor.data,
                location=form.location.data,
                date=form.date.data,
                time=form.time.data,
                notes=form.notes.data,
                remind=form.remind.data
            )
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment added successfully!', 'success')
            return redirect(url_for('calendar'))
        
        # Default to today's date
        if request.method == 'GET':
            form.date.data = date.today()
        
        # Get all appointments for JSON
        appointments = Appointment.query.filter_by(user_id=current_user.id).all()
        appt_list = []
        for appt in appointments:
            appt_datetime = datetime.combine(appt.date, appt.time)
            appt_list.append({
                'id': appt.id,
                'title': appt.title,
                'start': appt_datetime.isoformat(),
                'description': f"Doctor: {appt.doctor or 'N/A'}\nLocation: {appt.location or 'N/A'}\nNotes: {appt.notes or 'N/A'}"
            })
        
        # Get medications for calendar display
        medications = Medication.query.filter_by(user_id=current_user.id).all()
        med_events = []
        for med in medications:
            # Check if end_date exists, if not use today + 30 days for display purposes
            end_date = med.end_date if med.end_date else (date.today() + datetime.timedelta(days=30))
            
            # For simplicity, we'll just show a daily event for each medication
            # In a real app, you'd parse the time_of_day field and create specific events
            med_events.append({
                'id': f"med_{med.id}",
                'title': f"{med.name} - {med.dosage}",
                'start': med.start_date.isoformat(),
                'end': end_date.isoformat(),
                'description': f"Frequency: {med.frequency}\nNotes: {med.notes or 'N/A'}",
                'color': '#3788d8',  # Blue for medication events
                'allDay': True
            })
        
        # Combine both event types
        all_events = json.dumps(appt_list + med_events)
        
        return render_template('calendar.html', form=form, events=all_events)
    
    @app.route('/calendar/delete/<int:id>', methods=['POST'])
    @login_required
    def delete_appointment(id):
        appointment = Appointment.query.get_or_404(id)
        if appointment.user_id != current_user.id:
            flash('You are not authorized to delete this appointment.', 'danger')
            return redirect(url_for('calendar'))
        
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!', 'success')
        return redirect(url_for('calendar'))
    
    @app.route('/water_tracker', methods=['GET', 'POST'])
    @login_required
    def water_tracker():
        form = WaterIntakeForm()
        if form.validate_on_submit():
            water_intake = WaterIntake(
                user_id=current_user.id,
                amount=form.amount.data,
                date=date.today(),
                time=datetime.now().time()
            )
            db.session.add(water_intake)
            db.session.commit()
            flash('Water intake recorded successfully!', 'success')
            return redirect(url_for('water_tracker'))
        
        # Get today's water intake
        today_intake = WaterIntake.query.filter_by(
            user_id=current_user.id, 
            date=date.today()
        ).all()
        
        # Calculate total intake
        total_intake = sum(intake.amount for intake in today_intake)
        
        # Target amount (can be personalized in a real app)
        target_amount = 2000  # ml
        
        return render_template('water_tracker.html', 
                            form=form, 
                            intakes=today_intake,
                            total_intake=total_intake,
                            target_amount=target_amount)
    
    @app.route('/water_tracker/delete/<int:id>', methods=['POST'])
    @login_required
    def delete_water_intake(id):
        intake = WaterIntake.query.get_or_404(id)
        if intake.user_id != current_user.id:
            flash('You are not authorized to delete this entry.', 'danger')
            return redirect(url_for('water_tracker'))
        
        db.session.delete(intake)
        db.session.commit()
        flash('Water intake entry deleted successfully!', 'success')
        return redirect(url_for('water_tracker'))
    
    @app.route('/symptom_checker', methods=['GET', 'POST'])
    @login_required
    def symptom_checker():
        form = SymptomCheckerForm()
        results = None
        
        if form.validate_on_submit():
            # Process the symptoms
            symptoms = form.symptoms.data.lower()
            symptom_data = load_symptom_data()
            results = get_symptom_recommendations(symptoms, symptom_data)
            
        return render_template('symptom_checker.html', form=form, results=results)
    
    @app.route('/health_info')
    def health_info():
        articles = load_health_articles()
        return render_template('health_info.html', articles=articles)
    
    @app.route('/health_info/<article_id>')
    def article_detail(article_id):
        articles = load_health_articles()
        article = next((a for a in articles if a['id'] == article_id), None)
        if article:
            return render_template('article_detail.html', article=article)
        flash('Article not found', 'danger')
        return redirect(url_for('health_info'))
        
    @app.route('/sensor_data', methods=['GET', 'POST'])
    @login_required
    def sensor_data():
        """Page for ESP32 sensor data integration and visualization"""
        form = SensorDataForm()
        
        # Handle form submission for manual sensor data entry
        if form.validate_on_submit():
            new_reading = SensorData(
                user_id=current_user.id,
                sensor_type=form.sensor_type.data,
                value=form.value.data,
                unit=form.unit.data,
                device_id=form.device_id.data or "manual-entry",
                notes=form.notes.data
            )
            db.session.add(new_reading)
            db.session.commit()
            flash('Sensor reading recorded successfully!', 'success')
            return redirect(url_for('sensor_data'))
            
        # Handle incoming API data from ESP32
        elif request.method == 'POST' and request.is_json:
            sensor_data = request.get_json()
            if sensor_data and 'sensor_type' in sensor_data and 'value' in sensor_data and 'unit' in sensor_data:
                try:
                    new_reading = SensorData(
                        user_id=current_user.id,
                        sensor_type=sensor_data['sensor_type'],
                        value=float(sensor_data['value']),
                        unit=sensor_data['unit'],
                        device_id=sensor_data.get('device_id', 'esp32-device'),
                        notes=sensor_data.get('notes', '')
                    )
                    db.session.add(new_reading)
                    db.session.commit()
                    return jsonify({"status": "success", "message": "Data received and stored"}), 200
                except Exception as e:
                    return jsonify({"status": "error", "message": str(e)}), 400
            return jsonify({"status": "error", "message": "Invalid data format"}), 400
        
        # Get recent sensor readings
        recent_readings = SensorData.query.filter_by(
            user_id=current_user.id
        ).order_by(SensorData.timestamp.desc()).limit(100).all()
        
        # Group readings by sensor type for display
        readings_by_type = {}
        for reading in recent_readings:
            if reading.sensor_type not in readings_by_type:
                readings_by_type[reading.sensor_type] = []
            readings_by_type[reading.sensor_type].append(reading)
        
        # GET request - display the sensor dashboard
        return render_template('sensor_data.html', 
                              form=form, 
                              readings=recent_readings,
                              readings_by_type=readings_by_type)
    
    # API Endpoints for AJAX operations
    @app.route('/api/medications')
    @login_required
    def api_medications():
        medications = Medication.query.filter_by(user_id=current_user.id).all()
        med_list = []
        for med in medications:
            med_list.append({
                'id': med.id,
                'name': med.name,
                'dosage': med.dosage,
                'frequency': med.frequency,
                'start_date': med.start_date.isoformat(),
                'end_date': med.end_date.isoformat() if med.end_date else None,
                'time_of_day': med.time_of_day,
                'notes': med.notes
            })
        return jsonify(med_list)
    
    @app.route('/api/diet/<date_str>')
    @login_required
    def api_diet(date_str):
        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        
        entries = DietEntry.query.filter_by(
            user_id=current_user.id, 
            date=query_date
        ).all()
        
        entry_list = []
        for entry in entries:
            entry_list.append({
                'id': entry.id,
                'meal_type': entry.meal_type,
                'food_items': entry.food_items,
                'calories': entry.calories,
                'protein': entry.protein,
                'carbs': entry.carbs,
                'fat': entry.fat
            })
        
        # Calculate totals
        total_calories = sum(entry.calories or 0 for entry in entries)
        total_protein = sum(entry.protein or 0 for entry in entries)
        total_carbs = sum(entry.carbs or 0 for entry in entries)
        total_fat = sum(entry.fat or 0 for entry in entries)
        
        return jsonify({
            'entries': entry_list,
            'totals': {
                'calories': total_calories,
                'protein': total_protein,
                'carbs': total_carbs,
                'fat': total_fat
            }
        })
    
    @app.route('/api/water/<date_str>')
    @login_required
    def api_water(date_str):
        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        
        intakes = WaterIntake.query.filter_by(
            user_id=current_user.id, 
            date=query_date
        ).all()
        
        intake_list = []
        for intake in intakes:
            intake_list.append({
                'id': intake.id,
                'amount': intake.amount,
                'time': intake.time.strftime('%H:%M')
            })
        
        total_intake = sum(intake.amount for intake in intakes)
        
        return jsonify({
            'intakes': intake_list,
            'total': total_intake
        })
        
    @app.route('/api/sensor_data')
    @login_required
    def api_sensor_data():
        """API endpoint to retrieve sensor data"""
        # Get query parameters
        sensor_type = request.args.get('type')
        days = request.args.get('days', 7, type=int)  # Default to 7 days
        
        # Calculate the date range
        end_date = datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Base query
        query = SensorData.query.filter(
            SensorData.user_id == current_user.id,
            SensorData.timestamp >= start_date,
            SensorData.timestamp <= end_date
        )
        
        # Add filter for sensor type if provided
        if sensor_type:
            query = query.filter(SensorData.sensor_type == sensor_type)
        
        # Execute query and order by timestamp
        readings = query.order_by(SensorData.timestamp).all()
        
        # Format the data for API response
        readings_list = []
        for reading in readings:
            readings_list.append({
                'id': reading.id,
                'sensor_type': reading.sensor_type,
                'value': reading.value,
                'unit': reading.unit,
                'timestamp': reading.timestamp.isoformat(),
                'device_id': reading.device_id,
                'notes': reading.notes
            })
        
        return jsonify({
            'count': len(readings_list),
            'readings': readings_list
        })
        
    @app.route('/api/sensor_data/<int:id>', methods=['DELETE'])
    @login_required
    def delete_sensor_data(id):
        """API endpoint to delete a sensor reading"""
        reading = SensorData.query.get_or_404(id)
        if reading.user_id != current_user.id:
            return jsonify({'error': 'Not authorized'}), 403
        
        db.session.delete(reading)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Sensor reading deleted'})
        
    @app.route('/api/sensor_data/esp32', methods=['POST'])
    def esp32_sensor_data():
        """API endpoint for ESP32 devices to send sensor data"""
        if not request.is_json:
            return jsonify({'error': 'Expecting JSON data'}), 400
            
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['device_id', 'sensor_type', 'value', 'unit']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Create new sensor reading
            new_reading = SensorData(
                user_id=current_user.id if current_user.is_authenticated else 1,  # Default to user ID 1 if not authenticated
                sensor_type=data['sensor_type'],
                value=float(data['value']),
                unit=data['unit'],
                device_id=data['device_id'],
                notes=data.get('notes', '')
            )
            
            db.session.add(new_reading)
            db.session.commit()
            
            # Broadcast the new reading to all connected clients via WebSocket
            sensor_data = {
                'id': new_reading.id,
                'sensor_type': new_reading.sensor_type,
                'value': new_reading.value,
                'unit': new_reading.unit,
                'timestamp': new_reading.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'device_id': new_reading.device_id
            }
            
            socketio.emit('new_sensor_data', sensor_data)
            
            return jsonify({'success': True, 'id': new_reading.id})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    # SocketIO event handlers
    @socketio.on('connect')
    def handle_connect():
        print('Client connected to WebSocket')
        
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected from WebSocket')
