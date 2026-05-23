import time
import random
from devices.device_base import DeviceBase
from config import THRESHOLDS, UPDATE_INTERVAL

class PowerMeter(DeviceBase):
    """⚡ Power meter — voltage, current, energy consumption"""

    def __init__(self, token):
        super().__init__("PowerMeter", token)
        self.energy_kwh = 0.0
        self.voltage    = 220.0
        self.current    = 10.0

    def simulate(self):
        self.voltage = round(220.0 + random.gauss(0, 3), 2)
        self.current = round(10.0  + random.gauss(0, 0.5), 2)

        power_kw = round((self.voltage * self.current) / 1000, 3)
        self.energy_kwh += power_kw * (UPDATE_INTERVAL / 3600)

        if random.random() < 0.02:
            self.voltage += random.uniform(-20, 20)

        return {
            "voltage_v":      self.voltage,
            "current_amp":    self.current,
            "power_kw":       power_kw,
            "energy_kwh":     round(self.energy_kwh, 4),
            "status":         self.status,
            "undervolt_alert": self.voltage < THRESHOLDS["power_voltage_min"],
            "overvolt_alert":  self.voltage > THRESHOLDS["power_voltage_max"],
        }

    def run(self):
        while self.running:
            data = self.simulate()
            self.send_telemetry(data)
            status = "🔴 VOLT ALERT" if (data["undervolt_alert"] or
                                          data["overvolt_alert"]) else "🟢 OK"
            print(f"⚡ [{self.name}] {data['voltage_v']}V | "
                  f"{data['power_kw']}kW | {data['energy_kwh']}kWh {status}")
            time.sleep(UPDATE_INTERVAL)