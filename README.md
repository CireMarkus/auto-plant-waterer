# 🌱 Auto Plant Waterer

An automated plant care system built with Python and basic electronics. The Auto Plant Waterer monitors soil moisture, temperature, humidity, and ambient light — and performs actions based on sensor data, such as logging the readings to a NoSQL database. Perfect for smart home integration, remote gardening, or just keeping your plants healthy while you're away.

---

## 📌 Features

- 🟢 **Real-time Soil Moisture Monitoring** using analog sensors via MCP3008  
- 🌡️ **Temperature & Humidity Tracking** with the AHT20 sensor  
- 🌤️ **Ambient Light Sensing** via the VEML7700 (optional behavior triggers)  
- 📊 **Sensor Data Logging** to a NoSQL database (e.g., MongoDB) or terminal output  
- 🧪 **Test Mode** to simulate behavior without hardware activation  
- 🧱 **Modular Python Code** — easy to extend and maintain  

---

## 🛠️ Hardware Requirements

- **Raspberry Pi Zero** (W or WH recommended)  
- **MCP3008** analog-to-digital converter  
- **Capacitive Soil Moisture Sensor** ([example](https://www.amazon.com/Analog-Capacitive-Soil-Moisture-Sensor/dp/B09NTTR8M9))  
- **VEML7700** Lux Sensor (I²C)  
- **DHT22** Temperature & Humidity Sensor (I²C)  
- Jumper wires and breadboard (or soldered circuit)
---
## 📝 Key Scripts
1. LightSensor.py
   Measures ambient light intensity using the VEML7700 Lux Sensor.
   Automatically adjusts sensor sensitivity based on light conditions for accurate readings.
   Returns current light intensity in lux and voltage.

2. MoistureSensor.py
   Interfaces with a capacitive soil moisture sensor via MCP3008 ADC.
   Calibrates moisture levels, setting bounds for dry and wet soil conditions.
   Provides soil moisture level in voltage and ADC value.

3. TempHumSensor.py
   Reads temperature (°F) and humidity using the DHT22 sensor.
   Provides accurate environmental data for plant health monitoring.
---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/CireMarkus/auto-plant-waterer.git
cd auto-plant-waterer
```

### Configuration & Test Mode

- The project reads runtime configuration from `common/config.json`. Set the top-level
   `use_hardware` boolean to `true` to enable real hardware access, or `false` to force
   simulated sensors (useful for local development and CI).
