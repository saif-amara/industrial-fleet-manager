import time
from fleet.fleet_manager import FleetManager

def main():
    print("=" * 50)
    print("🏭  INDUSTRIAL IoT FLEET MANAGER")
    print("=" * 50)

    fleet = FleetManager()
    threads = fleet.start_all()

    try:
        while True:
            time.sleep(30)
            fleet.status()
    except KeyboardInterrupt:
        fleet.stop_all()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()