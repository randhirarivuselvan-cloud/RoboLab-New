COMPONENTS = [
 {"name":"Arduino Uno R3","category":"Arduino","price":550,"currency":"INR","description":"Beginner-friendly microcontroller board.","specifications":"ATmega328P, 5V logic","alternatives":["ESP32 DevKit V1"]},
 {"name":"ESP32 DevKit V1","category":"ESP32","price":450,"currency":"INR","description":"Wi-Fi/Bluetooth capable microcontroller.","specifications":"Dual-core MCU class, 3.3V logic","alternatives":["Arduino Uno R3"]},
 {"name":"HC-SR04 Ultrasonic Sensor","category":"Sensors","price":90,"currency":"INR","description":"Basic ultrasonic distance sensor.","specifications":"Ultrasonic ranging","alternatives":[]},
 {"name":"SG90 Servo","category":"Servos","price":130,"currency":"INR","description":"Small hobby servo for lightweight mechanisms.","specifications":"Micro servo; model-dependent torque","alternatives":["MG996R"]},
 {"name":"L298N Motor Driver","category":"Motor drivers","price":180,"currency":"INR","description":"Dual DC motor driver for starter builds.","specifications":"Dual H-bridge","alternatives":["TB6612FNG"]},
 {"name":"TB6612FNG Motor Driver","category":"Motor drivers","price":220,"currency":"INR","description":"Efficient dual DC motor driver.","specifications":"Dual H-bridge","alternatives":["L298N"]},
 {"name":"N20 Gear Motor","category":"Motors","price":180,"currency":"INR","description":"Small geared DC motor; verify voltage/RPM before purchase.","specifications":"Model-dependent voltage/RPM","alternatives":[]},
 {"name":"PCA9685 16-Channel PWM Driver","category":"Modules","price":180,"currency":"INR","description":"I2C PWM controller for multiple servos.","specifications":"16 PWM channels","alternatives":[]},
 {"name":"Raspberry Pi Zero 2 W","category":"Raspberry Pi","price":2200,"currency":"INR","description":"Compact Linux computer for higher-level software.","specifications":"Wi-Fi/Bluetooth, Linux","alternatives":[]},
]

def list_components(category=None):
    if not category: return COMPONENTS
    return [c for c in COMPONENTS if c["category"].lower() == category.lower()]

def recommend_components(idea: str):
    text = idea.lower()
    if any(x in text for x in ["line", "follow"]):
        names=["Arduino Uno R3","TB6612FNG Motor Driver","N20 Gear Motor","HC-SR04 Ultrasonic Sensor"]
    elif "quadruped" in text or "robot dog" in text:
        names=["ESP32 DevKit V1","PCA9685 16-Channel PWM Driver","SG90 Servo"]
    elif any(x in text for x in ["camera","vision","opencv","autonomous"]):
        names=["Raspberry Pi Zero 2 W","ESP32 DevKit V1","HC-SR04 Ultrasonic Sensor"]
    else:
        names=["ESP32 DevKit V1","HC-SR04 Ultrasonic Sensor","TB6612FNG Motor Driver"]
    return [c for c in COMPONENTS if c["name"] in names]
