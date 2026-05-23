import requests
import threading
from config import TB_BASE_URL, RPC_TIMEOUT

class DeviceBase:
    """Base class for all industrial devices"""

    def __init__(self, name, token):
        self.name    = name
        self.token   = token
        self.url     = f"{TB_BASE_URL}/{token}"
        self.running = False
        self.status  = "STOPPED"

    def send_telemetry(self, data):
        """Send telemetry data to ThingsBoard"""
        try:
            r = requests.post(f"{self.url}/telemetry", json=data, timeout=5)
            return r.status_code == 200
        except Exception as e:
            print(f"❌ [{self.name}] Telemetry error: {e}")
            return False

    def send_attribute(self, data):
        """Send device attributes to ThingsBoard"""
        try:
            r = requests.post(f"{self.url}/attributes", json=data, timeout=5)
            return r.status_code == 200
        except:
            return False

    def listen_rpc(self):
        """Listen for RPC commands from ThingsBoard dashboard"""
        print(f"👂 [{self.name}] Listening for RPC...")
        while self.running:
            try:
                r = requests.get(
                    f"{self.url}/rpc",
                    timeout=RPC_TIMEOUT
                )
                if r.status_code == 200:
                    cmd = r.json()
                    method = cmd.get("method", "")
                    print(f"📨 [{self.name}] RPC: {method}")
                    self.handle_rpc(cmd)
            except:
                pass

    def handle_rpc(self, cmd):
        """Override in subclass to handle RPC commands"""
        method = cmd.get("method", "")
        if method == "stop":
            self.status = "STOPPED"
            self.running = False
            print(f"🛑 [{self.name}] Stopped")
        elif method == "start":
            self.status = "RUNNING"
            print(f"▶️ [{self.name}] Started")

    def start(self):
        """Start device simulation"""
        self.running = True
        self.status  = "RUNNING"

        # RPC listener thread
        rpc_thread = threading.Thread(target=self.listen_rpc)
        rpc_thread.daemon = True
        rpc_thread.start()

        # Send initial attributes
        self.send_attribute({
            "device_name": self.name,
            "status":      self.status,
        })

        print(f"✅ [{self.name}] Started")
        self.run()

    def run(self):
        """Override in subclass — main simulation loop"""
        raise NotImplementedError