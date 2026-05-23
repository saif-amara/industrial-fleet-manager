# 🏭 Industrial IoT Fleet Manager

Real-time industrial device monitoring and control platform built on ThingsBoard IoT.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![ThingsBoard](https://img.shields.io/badge/ThingsBoard-4.x-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Devices](https://img.shields.io/badge/Devices-6-orange)
![Dashboard](assets/dashboard.png)

## 📋 Overview

Monitors **6 industrial devices** simultaneously with real-time telemetry,
anomaly detection, and remote control via RPC commands.

## 🏗️ Architecture

```
Fleet Manager
├── 🌡️  Temperature Sensor  → overheat detection
├── 📳  Vibration Sensor    → predictive maintenance
├── 🔵  Pressure Sensor     → leak detection
├── ⚙️   Motor Sensor        → overcurrent protection
├── ⚡  Power Meter         → energy monitoring
└── 🏗️  Conveyor Belt       → jam detection
```

## 📁 Project Structure

```
industrial-fleet-manager/
├── devices/
│   ├── device_base.py          # Base class for all devices
│   ├── temperature_sensor.py   # 🌡️ Temperature + overheat alert
│   ├── vibration_sensor.py     # 📳 Vibration + predictive maintenance
│   ├── pressure_sensor.py      # 🔵 Pressure + leak detection
│   ├── motor_sensor.py         # ⚙️  RPM + overcurrent protection
│   ├── power_meter.py          # ⚡ Voltage + energy monitoring
│   └── conveyor_belt.py        # 🏗️ Speed + load + jam detection
├── fleet/
│   └── fleet_manager.py        # Manages all devices concurrently
├── config.py                   # Tokens + thresholds configuration
├── main.py                     # Entry point
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Docker Desktop
- ThingsBoard CE

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/saif-amara/industrial-fleet-manager.git
cd industrial-fleet-manager

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start ThingsBoard
docker run -it -p 9090:9090 -p 1883:1883 \
  --name mytb --restart always \
  thingsboard/tb-postgres
```

### Configuration

Create 6 devices in ThingsBoard, then update `config.py`:

```python
DEVICE_TOKENS = {
    "temperature_sensor": "your_token_here",
    "vibration_sensor":   "your_token_here",
    "pressure_sensor":    "your_token_here",
    "motor_sensor":       "your_token_here",
    "power_meter":        "your_token_here",
    "conveyor_belt":      "your_token_here",
}
```

### Run

```bash
python main.py
```

## 📊 Monitored Parameters

| Device | Parameters | Alert Condition |
|--------|-----------|-----------------|
| 🌡️ Temperature | temp, setpoint | > 85°C |
| 📳 Vibration | RMS, frequency, wear | > 8 mm/s |
| 🔵 Pressure | bar, setpoint | < 0.5 or > 10 bar |
| ⚙️ Motor | RPM, current | current > 15A |
| ⚡ Power | voltage, kW, kWh | < 210V or > 240V |
| 🏗️ Conveyor | speed, load | speed < 0.1 m/s |

## 🔧 RPC Commands

| Device | Command | Description |
|--------|---------|-------------|
| Temperature | `set_setpoint` | Change target temperature |
| Vibration | `reset_wear` | Reset after maintenance |
| Motor | `set_rpm` | Change target RPM |
| Conveyor | `set_speed` | Change belt speed |
| All | `start` / `stop` | Start or stop device |

## 🎯 Applications

- Industrial automation monitoring
- Predictive maintenance systems
- Factory IoT infrastructure
- Embedded systems prototyping

## 👤 Author

**Saif Eddine Amara**
Embedded Systems Engineering Student — ISSAT Sousse, Tunisia
Teaching Assistant, Robotics Lab
