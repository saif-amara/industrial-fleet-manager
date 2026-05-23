import time
import random
from devices.device_base import DeviceBase
from config import THRESHOLDS, UPDATE_INTERVAL

class MotorSensor(DeviceBase):
    """⚙️ Motor speed sensor with overcurrent detection"""

    def __init__(self, token):
        super().__init__("MotorSensor", token)
        self.rpm     = 0.0
        self.current = 0.0
        self.target_rpm = 1500.0

    def simulate(self):
        drift = (self.target_rpm - self.rpm) * 0.1
        self.rpm += drift + random.gauss(0, 10)
        self.rpm  = round(max(0, self.rpm), 1)

        self.current = round(5.0 + (self.rpm / self.target_rpm) * 8.0
                             + random.gauss(0, 0.3), 2)

        if random.random() < 0.02:
            self.current += random.uniform(3, 8)

        return {
            "rpm":             self.rpm,
            "current_amp":     self.current,
            "target_rpm":      self.target_rpm,
            "status":          self.status,
            "overcurrent_alert": self.current > THRESHOLDS["motor_current_max"],
            "overspeed_alert": self.rpm > THRESHOLDS["motor_rpm_max"],
        }

    def handle_rpc(self, cmd):
        super().handle_rpc(cmd)
        method = cmd.get("method", "")
        if method == "set_rpm":
            self.target_rpm = cmd.get("params", {}).get("value", 1500.0)
            print(f"⚙️ [{self.name}] Target RPM → {self.target_rpm}")

    def run(self):
        while self.running:
            data = self.simulate()
            self.send_telemetry(data)
            status = "🔴 OVERCURRENT" if data["overcurrent_alert"] else "🟢 OK"
            print(f"⚙️  [{self.name}] {data['rpm']} RPM | {data['current_amp']}A {status}")
            time.sleep(UPDATE_INTERVAL)