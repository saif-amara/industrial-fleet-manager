import threading
from devices.temperature_sensor import TemperatureSensor
from devices.vibration_sensor   import VibrationSensor
from devices.pressure_sensor    import PressureSensor
from devices.motor_sensor       import MotorSensor
from devices.power_meter        import PowerMeter
from devices.conveyor_belt      import ConveyorBelt
from config import DEVICE_TOKENS

class FleetManager:
    """🏭 Manages all industrial devices"""

    def __init__(self):
        self.devices = {
            "temperature": TemperatureSensor(DEVICE_TOKENS["temperature_sensor"]),
            "vibration":   VibrationSensor(DEVICE_TOKENS["vibration_sensor"]),
            "pressure":    PressureSensor(DEVICE_TOKENS["pressure_sensor"]),
            "motor":       MotorSensor(DEVICE_TOKENS["motor_sensor"]),
            "power":       PowerMeter(DEVICE_TOKENS["power_meter"]),
            "conveyor":    ConveyorBelt(DEVICE_TOKENS["conveyor_belt"]),
        }

    def start_all(self):
        """Start all devices in separate threads"""
        print("🏭 Industrial Fleet Manager starting...")
        print(f"📡 Launching {len(self.devices)} devices...\n")

        threads = []
        for name, device in self.devices.items():
            t = threading.Thread(target=device.start)
            t.daemon = True
            threads.append(t)
            t.start()

        print("✅ All devices running!\n" + "="*50)
        return threads

    def stop_all(self):
        """Stop all devices"""
        for device in self.devices.values():
            device.running = False
        print("\n🛑 All devices stopped.")

    def status(self):
        """Print fleet status"""
        print("\n📊 Fleet Status:")
        for name, device in self.devices.items():
            print(f"  {name:15} → {device.status}")