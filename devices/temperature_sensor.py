import time
import random
from devices.device_base import DeviceBase
from config import THRESHOLDS, UPDATE_INTERVAL

class TemperatureSensor(DeviceBase):
    """🌡️ Industrial temperature sensor with overheat detection"""

    def __init__(self, token):
        super().__init__("TemperatureSensor", token)
        self.temperature = 25.0
        self.setpoint    = 70.0   # Target temperature

    def simulate(self):
        """Simulate realistic temperature changes"""
        # Slow drift toward setpoint with noise
        drift = (self.setpoint - self.temperature) * 0.05
        noise = random.gauss(0, 0.5)
        self.temperature += drift + noise
        self.temperature  = round(self.temperature, 2)

        # Occasional spike
        if random.random() < 0.02:
            self.temperature += random.uniform(10, 25)

        return {
            "temperature":    self.temperature,
            "setpoint":       self.setpoint,
            "status":         self.status,
            "overheat_alert": self.temperature > THRESHOLDS["temperature_max"],
        }

    def handle_rpc(self, cmd):
        super().handle_rpc(cmd)
        method = cmd.get("method", "")
        if method == "set_setpoint":
            self.setpoint = cmd.get("params", {}).get("value", 70.0)
            print(f"🌡️ [{self.name}] Setpoint → {self.setpoint}°C")

    def run(self):
        while self.running:
            data = self.simulate()
            self.send_telemetry(data)
            status = "🔴 OVERHEAT" if data["overheat_alert"] else "🟢 OK"
            print(f"🌡️  [{self.name}] {data['temperature']}°C {status}")
            time.sleep(UPDATE_INTERVAL)