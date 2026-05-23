import time
import random
import math
from devices.device_base import DeviceBase
from config import THRESHOLDS, UPDATE_INTERVAL

class VibrationSensor(DeviceBase):
    """📳 Industrial vibration sensor with predictive maintenance"""

    def __init__(self, token):
        super().__init__("VibrationSensor", token)
        self.time        = 0.0
        self.wear_level  = 0.0   # 0-100% machine wear
        self.frequency   = 50.0  # Hz

    def simulate(self):
        self.time       += UPDATE_INTERVAL
        self.wear_level += random.uniform(0, 0.01)  # slow wear
        self.wear_level  = min(self.wear_level, 100.0)

        # Vibration increases with wear
        base_vibration = 1.0 + (self.wear_level / 100) * 6.0
        noise          = random.gauss(0, 0.3)
        vibration      = abs(base_vibration + noise)

        # Frequency drift with wear
        self.frequency = 50.0 - (self.wear_level / 100) * 5.0

        # Anomaly spike
        if random.random() < 0.03:
            vibration += random.uniform(3, 8)

        vibration = round(vibration, 3)

        return {
            "vibration_rms":   vibration,
            "frequency_hz":    round(self.frequency, 2),
            "wear_level":      round(self.wear_level, 2),
            "status":          self.status,
            "anomaly_alert":   vibration > THRESHOLDS["vibration_max"],
            "maintenance_due": self.wear_level > 80.0,
        }

    def handle_rpc(self, cmd):
        super().handle_rpc(cmd)
        method = cmd.get("method", "")
        if method == "reset_wear":
            self.wear_level = 0.0
            print(f"🔧 [{self.name}] Wear level reset — Maintenance done!")

    def run(self):
        while self.running:
            data = self.simulate()
            self.send_telemetry(data)
            status = "🔴 ANOMALY" if data["anomaly_alert"] else "🟢 OK"
            maint  = " ⚠️ MAINTENANCE DUE" if data["maintenance_due"] else ""
            print(f"📳 [{self.name}] {data['vibration_rms']} mm/s {status}{maint}")
            time.sleep(UPDATE_INTERVAL)