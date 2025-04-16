from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms import DateField, TimeField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken. Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered. Please use a different email address.')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    gender = SelectField('Gender', choices=[
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not', 'Prefer not to say')
    ], validators=[Optional()])
    height = FloatField('Height (cm)', validators=[Optional()])
    weight = FloatField('Weight (kg)', validators=[Optional()])
    blood_type = SelectField('Blood Type', choices=[
        ('', 'Select Blood Type'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ], validators=[Optional()])
    allergies = TextAreaField('Allergies', validators=[Optional()])
    medical_conditions = TextAreaField('Medical Conditions', validators=[Optional()])
    submit = SubmitField('Update Profile')

class MedicationForm(FlaskForm):
    name = StringField('Medication Name', validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    frequency = SelectField('Frequency', choices=[
        ('daily', 'Daily'),
        ('twice_daily', 'Twice Daily'),
        ('three_times_daily', 'Three Times Daily'),
        ('weekly', 'Weekly'),
        ('as_needed', 'As Needed')
    ], validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[Optional()])
    time_of_day = StringField('Time(s) of Day', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Add Medication')

class DietEntryForm(FlaskForm):
    meal_type = SelectField('Meal Type', choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')
    ], validators=[DataRequired()])
    food_items = TextAreaField('Food Items', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[Optional()])
    protein = FloatField('Protein (g)', validators=[Optional()])
    carbs = FloatField('Carbs (g)', validators=[Optional()])
    fat = FloatField('Fat (g)', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Diet Entry')

class AppointmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    doctor = StringField('Doctor', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    remind = BooleanField('Set Reminder', default=True)
    submit = SubmitField('Add Appointment')

class WaterIntakeForm(FlaskForm):
    amount = IntegerField('Amount (ml)', validators=[DataRequired()])
    submit = SubmitField('Add Water Intake')

class CalorieEntryForm(FlaskForm):
    activity = StringField('Activity', validators=[DataRequired()])
    calories_burned = IntegerField('Calories Burned', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Calorie Entry')

class SymptomCheckerForm(FlaskForm):
    symptoms = TextAreaField('Describe your symptoms', validators=[DataRequired()])
    submit = SubmitField('Check Symptoms')

class SensorDataForm(FlaskForm):
    sensor_type = SelectField('Sensor Type', choices=[
        ('temperature', 'Temperature'),
        ('heart_rate', 'Heart Rate'),
        ('blood_pressure', 'Blood Pressure'),
        ('blood_oxygen', 'Blood Oxygen'),
        ('glucose', 'Blood Glucose'),
        ('ecg', 'Electrocardiogram (ECG)'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    unit = SelectField('Unit', choices=[
        ('celsius', '°C'),
        ('fahrenheit', '°F'),
        ('bpm', 'bpm'),
        ('mmHg', 'mmHg'),
        ('percent', '%'),
        ('mg/dL', 'mg/dL'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    device_id = StringField('Device ID', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Sensor Reading')
