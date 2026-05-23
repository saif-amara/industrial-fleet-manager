# ============================================
# Industrial Fleet Manager — Configuration
# ============================================

# ThingsBoard Settings
TB_HOST = "localhost"
TB_PORT = 9090
TB_BASE_URL = f"http://{TB_HOST}:{TB_PORT}/api/v1"

# Device Tokens — سنضيف token لكل device في ThingsBoard
DEVICE_TOKENS = {
    "temperature_sensor": "vyx22lk4ub0snwp0s2a7",
    "vibration_sensor":   "uGQAAnjpOXmVsbVB5efp",
    "pressure_sensor":    "NXfw75mTmhHmrpLx8bgS",
    "motor_sensor":       "veGBMJ3uAvggwFs46LPw",
    "power_meter":        "EkjxencsbLK3w3evF4w4",
    "conveyor_belt":      "W1L32FI9lXL7NZlVcHpO",
}

# Simulation Settings
UPDATE_INTERVAL = 1.0   # seconds between updates
RPC_TIMEOUT     = 30    # seconds for RPC long-polling

# Alarm Thresholds
THRESHOLDS = {
    "temperature_max":  85.0,   # °C
    "vibration_max":    8.0,    # mm/s
    "pressure_min":     0.5,    # bar
    "pressure_max":     10.0,   # bar
    "motor_rpm_max":    3000,   # RPM
    "motor_current_max": 15.0,  # Ampere
    "power_voltage_min": 210.0, # Volt
    "power_voltage_max": 240.0, # Volt
    "conveyor_speed_min": 0.1,  # m/s (jam detection)
}