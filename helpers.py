import json
import os
import re
from pathlib import Path

def load_health_articles():
    """
    Load health articles from the static data file.
    Returns a list of article dictionaries.
    """
    try:
        articles_file = Path(__file__).parent / 'static' / 'data' / 'health_articles.json'
        if articles_file.exists():
            with open(articles_file, 'r') as f:
                return json.load(f)
        else:
            # Return default articles if file doesn't exist
            return get_default_articles()
    except Exception as e:
        print(f"Error loading health articles: {e}")
        return get_default_articles()

def get_default_articles():
    """
    Return default health articles if the JSON file is not available.
    """
    return [
        {
            "id": "article1",
            "title": "Understanding Blood Pressure",
            "summary": "Learn about the importance of maintaining healthy blood pressure levels.",
            "content": """
                <h2>Understanding Blood Pressure</h2>
                <p>Blood pressure is the force of blood pushing against the walls of your arteries as your heart pumps blood. If this pressure rises and stays high over time, it can damage your heart and lead to health problems, such as heart disease and stroke.</p>
                
                <h3>Blood Pressure Readings</h3>
                <p>Blood pressure is measured using two numbers:</p>
                <ul>
                    <li><strong>Systolic pressure</strong> (the top number) - represents the pressure in your arteries when your heart beats</li>
                    <li><strong>Diastolic pressure</strong> (the bottom number) - represents the pressure in your arteries when your heart rests between beats</li>
                </ul>
                
                <h3>Blood Pressure Categories</h3>
                <ul>
                    <li><strong>Normal:</strong> Less than 120/80 mm Hg</li>
                    <li><strong>Elevated:</strong> Systolic between 120-129 and diastolic less than 80</li>
                    <li><strong>Stage 1 Hypertension:</strong> Systolic between 130-139 or diastolic between 80-89</li>
                    <li><strong>Stage 2 Hypertension:</strong> Systolic at least 140 or diastolic at least 90</li>
                </ul>
                
                <h3>Tips for Maintaining Healthy Blood Pressure</h3>
                <ul>
                    <li>Maintain a healthy weight</li>
                    <li>Exercise regularly</li>
                    <li>Eat a healthy diet that's low in salt, saturated fat, and added sugars</li>
                    <li>Limit alcohol consumption</li>
                    <li>Quit smoking</li>
                    <li>Manage stress</li>
                    <li>Take medications as prescribed</li>
                </ul>
            """,
            "category": "Heart Health",
            "author": "Dr. Sarah Johnson",
            "date": "2023-01-15"
        },
        {
            "id": "article2",
            "title": "The Importance of Staying Hydrated",
            "summary": "Discover why water is essential for your body and how to ensure you're getting enough.",
            "content": """
                <h2>The Importance of Staying Hydrated</h2>
                <p>Water is essential for nearly every bodily function. It makes up about 60% of your body weight and is involved in many important processes including regulating body temperature, carrying nutrients to cells, and flushing toxins.</p>
                
                <h3>Benefits of Proper Hydration</h3>
                <ul>
                    <li>Improves physical performance</li>
                    <li>Boosts energy levels and brain function</li>
                    <li>Helps prevent and treat headaches</li>
                    <li>Aids digestion and prevents constipation</li>
                    <li>May help with weight management</li>
                    <li>Keeps skin healthy</li>
                </ul>
                
                <h3>How Much Water Should You Drink?</h3>
                <p>The common recommendation is to drink eight 8-ounce glasses of water per day (about 2 liters or half a gallon). However, individual needs vary based on activity level, climate, health status, and other factors.</p>
                
                <h3>Signs of Dehydration</h3>
                <ul>
                    <li>Thirst</li>
                    <li>Dark yellow urine</li>
                    <li>Fatigue</li>
                    <li>Dizziness</li>
                    <li>Dry mouth and lips</li>
                    <li>Headache</li>
                </ul>
                
                <h3>Tips for Staying Hydrated</h3>
                <ul>
                    <li>Carry a reusable water bottle</li>
                    <li>Set reminders to drink water throughout the day</li>
                    <li>Drink water before, during, and after exercise</li>
                    <li>Consume water-rich foods like fruits and vegetables</li>
                    <li>Flavor water with fruits or herbs if you don't like plain water</li>
                </ul>
            """,
            "category": "Nutrition",
            "author": "Dr. Michael Chen",
            "date": "2023-02-10"
        },
        {
            "id": "article3",
            "title": "Managing Diabetes Through Diet",
            "summary": "Learn how dietary choices affect blood sugar levels and how to manage diabetes through nutrition.",
            "content": """
                <h2>Managing Diabetes Through Diet</h2>
                <p>Diet plays a crucial role in managing diabetes. The food you eat directly affects your blood sugar levels, so making informed food choices is essential for controlling the condition.</p>
                
                <h3>Key Dietary Principles for Diabetes Management</h3>
                <ul>
                    <li><strong>Carbohydrate Counting:</strong> Track the amount of carbs you eat to help manage blood sugar levels</li>
                    <li><strong>Glycemic Index:</strong> Choose foods with a low or medium glycemic index</li>
                    <li><strong>Portion Control:</strong> Be mindful of portion sizes to prevent overeating</li>
                    <li><strong>Regular Meal Timing:</strong> Eat meals and snacks at consistent times</li>
                </ul>
                
                <h3>Foods to Include</h3>
                <ul>
                    <li>Non-starchy vegetables (spinach, broccoli, carrots)</li>
                    <li>Whole grains (brown rice, oats, quinoa)</li>
                    <li>Lean proteins (chicken, fish, tofu)</li>
                    <li>Healthy fats (avocados, nuts, olive oil)</li>
                    <li>Low-fat dairy or alternatives</li>
                    <li>Fruits in moderation</li>
                </ul>
                
                <h3>Foods to Limit</h3>
                <ul>
                    <li>Refined carbohydrates (white bread, white rice)</li>
                    <li>Sugary beverages and foods</li>
                    <li>Processed meats</li>
                    <li>Fried foods and foods high in saturated or trans fats</li>
                    <li>Alcoholic beverages</li>
                </ul>
                
                <h3>Sample Meal Plan</h3>
                <p><strong>Breakfast:</strong> Overnight oats with berries and nuts</p>
                <p><strong>Lunch:</strong> Grilled chicken salad with olive oil dressing</p>
                <p><strong>Snack:</strong> Apple slices with a tablespoon of peanut butter</p>
                <p><strong>Dinner:</strong> Baked salmon with roasted vegetables and quinoa</p>
                
                <p><em>Note: Always consult with your healthcare provider or a registered dietitian before making significant changes to your diet, especially if you have diabetes.</em></p>
            """,
            "category": "Diabetes",
            "author": "Dr. Emily Rodriguez",
            "date": "2023-03-05"
        }
    ]

def load_symptom_data():
    """
    Load symptom data from the static data file.
    Returns a dictionary mapping symptoms to possible conditions and recommendations.
    """
    try:
        symptom_file = Path(__file__).parent / 'static' / 'data' / 'symptom_data.json'
        if symptom_file.exists():
            with open(symptom_file, 'r') as f:
                return json.load(f)
        else:
            # Return default symptom data if file doesn't exist
            return get_default_symptom_data()
    except Exception as e:
        print(f"Error loading symptom data: {e}")
        return get_default_symptom_data()

def get_default_symptom_data():
    """
    Return default symptom data if the JSON file is not available.
    """
    return {
        "headache": {
            "possible_conditions": ["Tension headache", "Migraine", "Dehydration", "Sinusitis"],
            "recommendations": [
                "Rest in a quiet, dark room",
                "Apply a cold or warm compress to your head",
                "Stay hydrated",
                "Over-the-counter pain relievers like acetaminophen or ibuprofen may help"
            ],
            "when_to_see_doctor": [
                "Severe or sudden headache",
                "Headache with fever, stiff neck, confusion, seizures, double vision, weakness, numbness or difficulty speaking",
                "Headache after a head injury",
                "Chronic or recurring headaches"
            ]
        },
        "fever": {
            "possible_conditions": ["Viral infection", "Bacterial infection", "Inflammatory conditions"],
            "recommendations": [
                "Rest and stay hydrated",
                "Take acetaminophen or ibuprofen to reduce fever",
                "Use a light blanket if you have chills"
            ],
            "when_to_see_doctor": [
                "Temperature above 103°F (39.4°C)",
                "Fever lasting more than three days",
                "Fever with severe headache, stiff neck, confusion or difficulty breathing",
                "Fever in infants and young children"
            ]
        },
        "cough": {
            "possible_conditions": ["Common cold", "Flu", "Allergies", "Asthma", "Bronchitis"],
            "recommendations": [
                "Stay hydrated",
                "Use a humidifier or take a steamy shower",
                "Honey (for adults and children over 1 year)",
                "Over-the-counter cough suppressants for dry coughs",
                "Over-the-counter expectorants for productive coughs"
            ],
            "when_to_see_doctor": [
                "Cough lasting more than three weeks",
                "Coughing up blood or yellow-green phlegm",
                "Cough with fever, chest pain, or difficulty breathing",
                "Cough that disturbs sleep or daily activities"
            ]
        },
        "sore throat": {
            "possible_conditions": ["Common cold", "Strep throat", "Tonsillitis", "Allergies"],
            "recommendations": [
                "Gargle with warm salt water",
                "Drink warm liquids like tea with honey",
                "Use throat lozenges or sprays",
                "Take acetaminophen or ibuprofen for pain"
            ],
            "when_to_see_doctor": [
                "Severe pain when swallowing",
                "Sore throat with fever over 101°F (38.3°C)",
                "Sore throat lasting more than a week",
                "Rash, joint pain, or difficulty breathing"
            ]
        },
        "stomach pain": {
            "possible_conditions": ["Indigestion", "Gas", "Food poisoning", "Gastritis", "Appendicitis"],
            "recommendations": [
                "Avoid solid foods for a few hours",
                "Sip clear liquids like water or broth",
                "Avoid dairy, caffeine, alcohol, and fatty foods",
                "Use a heating pad on your abdomen"
            ],
            "when_to_see_doctor": [
                "Severe or persistent pain",
                "Pain accompanied by fever",
                "Inability to keep food down for more than 2 days",
                "Bloody stools or vomit",
                "Pain during pregnancy"
            ]
        },
        "nausea": {
            "possible_conditions": ["Food poisoning", "Gastroenteritis", "Migraine", "Medication side effect"],
            "recommendations": [
                "Eat bland foods like crackers or toast",
                "Drink clear liquids in small sips",
                "Avoid strong odors and foods",
                "Ginger tea or ginger supplements"
            ],
            "when_to_see_doctor": [
                "Nausea lasting more than 2 days",
                "Inability to keep any food or liquid down",
                "Signs of dehydration (dark urine, dizziness)",
                "Severe abdominal pain"
            ]
        },
        "fatigue": {
            "possible_conditions": ["Lack of sleep", "Stress", "Anemia", "Depression", "Hypothyroidism"],
            "recommendations": [
                "Ensure adequate sleep (7-9 hours)",
                "Stay hydrated and eat balanced meals",
                "Regular physical activity",
                "Stress management techniques"
            ],
            "when_to_see_doctor": [
                "Persistent fatigue despite adequate rest",
                "Fatigue with unexplained weight loss",
                "Fatigue with shortness of breath or chest pain",
                "Extreme fatigue that interferes with daily activities"
            ]
        },
        "dizziness": {
            "possible_conditions": ["Dehydration", "Low blood sugar", "Inner ear issues", "Low blood pressure"],
            "recommendations": [
                "Sit or lie down immediately",
                "Stay hydrated",
                "Eat regular meals",
                "Avoid sudden movements"
            ],
            "when_to_see_doctor": [
                "Persistent or severe dizziness",
                "Dizziness with headache, hearing loss, or ringing in ears",
                "Dizziness with chest pain or irregular heartbeat",
                "Dizziness after a head injury"
            ]
        }
    }

def get_symptom_recommendations(user_input, symptom_data):
    """
    Match user input with known symptoms and return relevant information.
    """
    result = {
        "matched_symptoms": [],
        "possible_conditions": set(),
        "recommendations": set(),
        "when_to_see_doctor": set()
    }
    
    # Look for keywords in the user input
    for symptom, data in symptom_data.items():
        if re.search(r'\b' + re.escape(symptom) + r'\b', user_input, re.IGNORECASE):
            result["matched_symptoms"].append(symptom)
            result["possible_conditions"].update(data["possible_conditions"])
            result["recommendations"].update(data["recommendations"])
            result["when_to_see_doctor"].update(data["when_to_see_doctor"])
    
    # Convert sets to lists for JSON serialization
    result["possible_conditions"] = list(result["possible_conditions"])
    result["recommendations"] = list(result["recommendations"])
    result["when_to_see_doctor"] = list(result["when_to_see_doctor"])
    
    # Add disclaimer
    result["disclaimer"] = "This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition."
    
    return result
