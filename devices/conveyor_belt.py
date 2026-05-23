import time
import random
from devices.device_base import DeviceBase
from config import THRESHOLDS, UPDATE_INTERVAL

class ConveyorBelt(DeviceBase):
    """🏗️ Conveyor belt monitor — speed, load, jam detection"""

    def __init__(self, token):
        super().__init__("ConveyorBelt", token)
        self.speed      = 1.0
        self.load       = 0.0
        self.target_speed = 1.2

    def simulate(self):
        drift = (self.target_speed - self.speed) * 0.1
        self.speed = round(max(0, self.speed + drift + random.gauss(0, 0.02)), 3)
        self.load  = round(random.uniform(20, 90) + random.gauss(0, 5), 2)

        jammed = self.speed < THRESHOLDS["conveyor_speed_min"] and self.load > 50

        if random.random() < 0.02:
            self.speed = 0.0

        return {
            "speed_ms":      self.speed,
            "load_percent":  self.load,
            "target_speed":  self.target_speed,
            "status":        self.status,
            "jam_alert":     jammed,
            "overload_alert": self.load > 95.0,
        }

    def handle_rpc(self, cmd):
        super().handle_rpc(cmd)
        method = cmd.get("method", "")
        if method == "set_speed":
            self.target_speed = cmd.get("params", {}).get("value", 1.2)
            print(f"🏗️ [{self.name}] Target speed → {self.target_speed} m/s")

    def run(self):
        while self.running:
            data = self.simulate()
            self.send_telemetry(data)
            status = "🔴 JAM" if data["jam_alert"] else "🟢 OK"
            print(f"🏗️  [{self.name}] {data['speed_ms']} m/s | "
                  f"{data['load_percent']}% load {status}")
            time.sleep(UPDATE_INTERVAL)