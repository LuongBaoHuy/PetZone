/*
 * PetZone ESP32 - IoT Device Controller
 * =====================================
 * Nhận lệnh từ AI Service và điều khiển Fan, Heater, Humidifier
 */

#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

// ========== WIFI CONFIGURATION ==========
const char* ssid = "YOUR_WIFI_SSID";         // Thay bằng WiFi của bạn
const char* password = "YOUR_WIFI_PASSWORD"; // Thay bằng password WiFi

// ========== PIN CONFIGURATION ==========
const int FAN_PIN = 25;          // PWM pin cho quạt
const int HEATER_PIN = 26;       // PWM pin cho máy sưởi
const int HUMIDIFIER_PIN = 27;   // PWM pin cho máy phun sương
const int LED_PIN = 2;           // LED indicator

// ========== WEB SERVER ==========
WebServer server(80);

// ========== DEVICE STATES ==========
struct DeviceState {
  bool isOn;
  int intensity;  // 0-100
};

DeviceState fanState = {false, 0};
DeviceState heaterState = {false, 0};
DeviceState humidifierState = {false, 0};

// ========== SETUP ==========
void setup() {
  Serial.begin(115200);
  
  // Setup pins
  pinMode(FAN_PIN, OUTPUT);
  pinMode(HEATER_PIN, OUTPUT);
  pinMode(HUMIDIFIER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  
  // Initial state: all off
  analogWrite(FAN_PIN, 0);
  analogWrite(HEATER_PIN, 0);
  analogWrite(HUMIDIFIER_PIN, 0);
  
  Serial.println("\n========================================");
  Serial.println("🐾 PetZone ESP32 IoT Controller");
  Serial.println("========================================");
  
  // Connect to WiFi
  connectToWiFi();
  
  // Setup web server endpoints
  server.on("/", HTTP_GET, handleRoot);
  server.on("/control", HTTP_POST, handleControl);
  server.on("/status", HTTP_GET, handleStatus);
  server.on("/test", HTTP_GET, handleTest);
  
  server.begin();
  
  Serial.println("\n✅ Web Server started!");
  Serial.print("📡 ESP32 IP: http://");
  Serial.println(WiFi.localIP());
  Serial.println("\nEndpoints:");
  Serial.println("  GET  /         - Home page");
  Serial.println("  POST /control  - Control devices");
  Serial.println("  GET  /status   - Get device status");
  Serial.println("  GET  /test     - Test all devices");
  Serial.println("========================================\n");
}

// ========== MAIN LOOP ==========
void loop() {
  server.handleClient();
  
  // Blink LED để show hoạt động
  static unsigned long lastBlink = 0;
  if (millis() - lastBlink > 1000) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    lastBlink = millis();
  }
}

// ========== WIFI CONNECTION ==========
void connectToWiFi() {
  Serial.print("🌐 Connecting to WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi connected!");
    Serial.print("📡 IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ WiFi connection failed!");
    Serial.println("⚠️  Running in offline mode...");
  }
}

// ========== WEB SERVER HANDLERS ==========

// Root endpoint - Home page
void handleRoot() {
  String html = "<html><head><title>PetZone ESP32</title>";
  html += "<style>body{font-family:Arial;margin:20px;background:#f0f0f0;}";
  html += ".card{background:white;padding:20px;margin:10px 0;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);}";
  html += ".on{color:green;} .off{color:red;}</style></head><body>";
  html += "<h1>🐾 PetZone IoT Controller</h1>";
  
  html += "<div class='card'><h2>Device Status</h2>";
  html += "<p>🌀 Fan: <span class='" + String(fanState.isOn ? "on'>ON" : "off'>OFF") + "</span> (" + String(fanState.intensity) + "%)</p>";
  html += "<p>🔥 Heater: <span class='" + String(heaterState.isOn ? "on'>ON" : "off'>OFF") + "</span> (" + String(heaterState.intensity) + "%)</p>";
  html += "<p>💧 Humidifier: <span class='" + String(humidifierState.isOn ? "on'>ON" : "off'>OFF") + "</span> (" + String(humidifierState.intensity) + "%)</p>";
  html += "</div>";
  
  html += "<div class='card'><h2>API Endpoints</h2>";
  html += "<p><code>POST /control</code> - Control devices</p>";
  html += "<p><code>GET /status</code> - Get device status</p>";
  html += "<p><code>GET /test</code> - Test all devices</p>";
  html += "</div>";
  
  html += "<div class='card'><p>ESP32 IP: " + WiFi.localIP().toString() + "</p></div>";
  html += "</body></html>";
  
  server.send(200, "text/html", html);
}

// Control endpoint - Nhận lệnh từ AI Service
void handleControl() {
  Serial.println("\n========== CONTROL REQUEST ==========");
  
  if (server.hasArg("plain")) {
    String body = server.arg("plain");
    Serial.println("📥 Received: " + body);
    
    // Parse JSON
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, body);
    
    if (error) {
      Serial.println("❌ JSON parse failed!");
      server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"Invalid JSON\"}");
      return;
    }
    
    String device = doc["device"];
    int state = doc["state"];  // 0 = OFF, 1 = ON
    int intensity = doc["intensity"] | 100;  // Default 100%
    
    Serial.println("🎮 Device: " + device);
    Serial.println("⚡ State: " + String(state ? "ON" : "OFF"));
    Serial.println("💪 Intensity: " + String(intensity) + "%");
    
    // Control devices
    bool success = false;
    if (device == "fan") {
      success = controlFan(state, intensity);
    } else if (device == "heater") {
      success = controlHeater(state, intensity);
    } else if (device == "humidifier") {
      success = controlHumidifier(state, intensity);
    } else {
      Serial.println("❌ Unknown device: " + device);
      server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"Unknown device\"}");
      return;
    }
    
    if (success) {
      String response = "{\"status\":\"success\",\"device\":\"" + device + "\",\"state\":" + String(state) + ",\"intensity\":" + String(intensity) + "}";
      server.send(200, "application/json", response);
      Serial.println("✅ Command executed successfully!");
    } else {
      server.send(500, "application/json", "{\"status\":\"error\",\"message\":\"Failed to control device\"}");
      Serial.println("❌ Command execution failed!");
    }
    
  } else {
    server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"No body\"}");
    Serial.println("❌ No request body!");
  }
  
  Serial.println("====================================\n");
}

// Status endpoint - Trả về trạng thái hiện tại
void handleStatus() {
  StaticJsonDocument<256> doc;
  
  JsonObject fan = doc.createNestedObject("fan");
  fan["isOn"] = fanState.isOn;
  fan["intensity"] = fanState.intensity;
  
  JsonObject heater = doc.createNestedObject("heater");
  heater["isOn"] = heaterState.isOn;
  heater["intensity"] = heaterState.intensity;
  
  JsonObject humidifier = doc.createNestedObject("humidifier");
  humidifier["isOn"] = humidifierState.isOn;
  humidifier["intensity"] = humidifierState.intensity;
  
  doc["uptime"] = millis() / 1000;
  doc["wifi_rssi"] = WiFi.RSSI();
  
  String response;
  serializeJson(doc, response);
  
  server.send(200, "application/json", response);
  Serial.println("📊 Status sent: " + response);
}

// Test endpoint - Test tất cả thiết bị
void handleTest() {
  Serial.println("\n🧪 Testing all devices...");
  
  // Test Fan
  Serial.println("Testing Fan...");
  controlFan(1, 50);
  delay(2000);
  controlFan(0, 0);
  
  // Test Heater
  Serial.println("Testing Heater...");
  controlHeater(1, 50);
  delay(2000);
  controlHeater(0, 0);
  
  // Test Humidifier
  Serial.println("Testing Humidifier...");
  controlHumidifier(1, 50);
  delay(2000);
  controlHumidifier(0, 0);
  
  server.send(200, "application/json", "{\"status\":\"success\",\"message\":\"Test completed\"}");
  Serial.println("✅ Test completed!\n");
}

// ========== DEVICE CONTROL FUNCTIONS ==========

bool controlFan(int state, int intensity) {
  fanState.isOn = (state == 1);
  fanState.intensity = intensity;
  
  if (fanState.isOn) {
    int pwmValue = map(intensity, 0, 100, 0, 255);
    analogWrite(FAN_PIN, pwmValue);
    Serial.println("🌀 Fan ON at " + String(intensity) + "% (PWM: " + String(pwmValue) + ")");
  } else {
    analogWrite(FAN_PIN, 0);
    Serial.println("🌀 Fan OFF");
  }
  
  return true;
}

bool controlHeater(int state, int intensity) {
  heaterState.isOn = (state == 1);
  heaterState.intensity = intensity;
  
  if (heaterState.isOn) {
    int pwmValue = map(intensity, 0, 100, 0, 255);
    analogWrite(HEATER_PIN, pwmValue);
    Serial.println("🔥 Heater ON at " + String(intensity) + "% (PWM: " + String(pwmValue) + ")");
  } else {
    analogWrite(HEATER_PIN, 0);
    Serial.println("🔥 Heater OFF");
  }
  
  return true;
}

bool controlHumidifier(int state, int intensity) {
  humidifierState.isOn = (state == 1);
  humidifierState.intensity = intensity;
  
  if (humidifierState.isOn) {
    int pwmValue = map(intensity, 0, 100, 0, 255);
    analogWrite(HUMIDIFIER_PIN, pwmValue);
    Serial.println("💧 Humidifier ON at " + String(intensity) + "% (PWM: " + String(pwmValue) + ")");
  } else {
    analogWrite(HUMIDIFIER_PIN, 0);
    Serial.println("💧 Humidifier OFF");
  }
  
  return true;
}
