/**
 * ESP32 + DHT11 Temperature/Humidity Sensor Example
 * Sends data to health tracker application using WebSocket API
 */
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// Your health app API endpoint
const char* serverUrl = "http://your-replit-app-url.repl.co/api/sensor_data/esp32";

// Device identifier
const char* deviceId = "esp32-dht11-01"; 

// DHT11 sensor configuration
#define DHTPIN 4      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11 // DHT 11
DHT dht(DHTPIN, DHTTYPE);

// Time between readings (milliseconds)
const unsigned long READING_INTERVAL = 30000; // 30 seconds
unsigned long lastReadingTime = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 DHT11 Health Tracker Example");
  
  // Initialize DHT sensor
  dht.begin();
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  unsigned long currentTime = millis();
  
  // Check if it's time to read the sensor
  if (currentTime - lastReadingTime >= READING_INTERVAL) {
    lastReadingTime = currentTime;
    
    // Read temperature and humidity
    float temperature = dht.readTemperature(); // in Celsius
    float humidity = dht.readHumidity();
    
    // Check if readings are valid
    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    
    // Print readings to serial
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print("°C, Humidity: ");
    Serial.print(humidity);
    Serial.println("%");
    
    // Send temperature data
    sendSensorData("temperature", temperature, "celsius");
    
    // Wait a bit before sending humidity
    delay(2000);
    
    // Send humidity data
    sendSensorData("humidity", humidity, "percent");
  }
}

void sendSensorData(const char* sensorType, float value, const char* unit) {
  // Check WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected. Reconnecting...");
    WiFi.begin(ssid, password);
    delay(5000);
    return;
  }
  
  // Create JSON document
  StaticJsonDocument<200> doc;
  doc["sensor_type"] = sensorType;
  doc["value"] = value;
  doc["unit"] = unit;
  doc["device_id"] = deviceId;
  doc["notes"] = "DHT11 sensor reading";
  
  // Serialize JSON to string
  String jsonString;
  serializeJson(doc, jsonString);
  
  // Send HTTP POST request
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("HTTP Response code: " + String(httpResponseCode));
    Serial.println(response);
  } else {
    Serial.println("Error sending HTTP request. Code: " + String(httpResponseCode));
  }
  
  http.end();
}