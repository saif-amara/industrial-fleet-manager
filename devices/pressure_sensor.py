import time
import random
from devices.device_base import DeviceBase
from config import THRESHOLDS, UPDATE_INTERVAL

class PressureSensor(DeviceBase):
    """🔵 Industrial pressure sensor with leak detection"""

    def __init__(self, token):
        super().__init__("PressureSensor", token)
        self.pressure = 5.0
        self.setpoint = 6.0

    def simulate(self):
        drift = (self.setpoint - self.pressure) * 0.1
        noise = random.gauss(0, 0.1)
        self.pressure += drift + noise
        self.pressure  = round(max(0, self.pressure), 3)

        if random.random() < 0.02:
            self.pressure -= random.uniform(1, 3)

        return {
            "pressure_bar":  self.pressure,
            "setpoint":      self.setpoint,
            "status":        self.status,
            "leak_alert":    self.pressure < THRESHOLDS["pressure_min"],
            "overpress_alert": self.pressure > THRESHOLDS["pressure_max"],
        }

    def run(self):
        while self.running:
            data = self.simulate()
            self.send_telemetry(data)
            status = "🔴 LEAK" if data["leak_alert"] else "🟢 OK"
            print(f"🔵 [{self.name}] {data['pressure_bar']} bar {status}")
            time.sleep(UPDATE_INTERVAL)