# smart_home_system.py
from repositories import DeviceRepository, UserRepository, AutomationRepository
from devices import Device
from users import UserFactory
from rules import AutomationRule
from notifications import notification_service
from reports import ReportService
from interceptor import Interceptor
from logger import logger
import time

# Resource Pool Pattern (for simplicity, pool of Device objects ready to use)
class DevicePool:
    def __init__(self, size=5):
        self._pool = [Device(i, f"Preloaded Device {i}", "Generic") for i in range(1000, 1000 + size)]

    def acquire(self):
        if self._pool:
            return self._pool.pop(0)
        else:
            logger.log("No devices available in pool")
            return None

    def release(self, device):
        self._pool.append(device)

device_pool = DevicePool()

# Microservice Decomposition: each repo/service acts like a microservice
device_repo = DeviceRepository()
user_repo = UserRepository()
automation_repo = AutomationRepository()
report_service = ReportService(device_repo, automation_repo, user_repo)
interceptor = Interceptor()

def device_menu():
    while True:
        print("\n-- Device Management --")
        print("1. Add Device from Pool")
        print("2. Update Device")
        print("3. Delete Device")
        print("4. View Devices")
        print("5. Back")
        choice = input("Option: ")

        try:
            if choice == '1':
                interceptor.pre_process("Add Device")
                device = device_pool.acquire()
                if device:
                    device.name = input("Enter Device Name: ")
                    device.device_type = input("Enter Device Type: ")
                    device_repo.add_device(device)
                interceptor.post_process("Add Device")

            elif choice == '2':
                device_id = int(input("Enter Device ID: "))
                status = input("New Status (ON/OFF): ")
                interceptor.pre_process("Update Device")
                device_repo.update_device(device_id, status=status)
                interceptor.post_process("Update Device")

            elif choice == '3':
                device_id = int(input("Enter Device ID: "))
                device = device_repo.get_device(device_id)
                if device:
                    interceptor.pre_process("Delete Device")
                    device_repo.delete_device(device_id)
                    device_pool.release(device)
                    interceptor.post_process("Delete Device")

            elif choice == '4':
                for d in device_repo.devices.values():
                    print(f"{d.device_id} - {d.name}, {d.device_type}, Status: {d.status}")
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            logger.log(f"Error: {e}")

def user_menu():
    while True:
        print("\n-- User Management --")
        print("1. Register User")
        print("2. Delete User")
        print("3. View Users")
        print("4. Back")
        choice = input("Option: ")

        try:
            if choice == '1':
                interceptor.pre_process("Register User")
                user_id = int(input("User ID: "))
                name = input("Name: ")
                role = input("Role (HomeOwner/Admin): ")
                user = UserFactory.create_user(role, user_id, name)
                user_repo.add_user(user)
                notification_service.subscribe(user)
                interceptor.post_process("Register User")

            elif choice == '2':
                user_id = int(input("User ID to delete: "))
                user = user_repo.get_user(user_id)
                if user:
                    interceptor.pre_process("Delete User")
                    notification_service.unsubscribe(user)
                    user_repo.delete_user(user_id)
                    interceptor.post_process("Delete User")

            elif choice == '3':
                for u in user_repo.users.values():
                    print(f"{u.user_id} - {u.name} ({u.__class__.__name__})")
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            logger.log(f"Error: {e}")

def automation_menu():
    while True:
        print("\n-- Automation Rules --")
        print("1. Add Rule")
        print("2. Evaluate Rules")
        print("3. Delete Rule")
        print("4. View Rules")
        print("5. Back")
        choice = input("Option: ")

        try:
            if choice == '1':
                rule_id = int(input("Rule ID: "))
                device_id = int(input("Device ID: "))
                action_type = input("Action (turn_on/turn_off): ")

                def condition(dev=device_repo.get_device(device_id)):
                    return dev.status == "OFF" if action_type == "turn_on" else dev.status == "ON"

                def action(dev=device_repo.get_device(device_id)):
                    dev.status = "ON" if action_type == "turn_on" else "OFF"
                    logger.log(f"Rule {rule_id}: Executed - {dev.name} is now {dev.status}")

                rule = AutomationRule(rule_id, condition, action)
                automation_repo.add_rule(rule)

            elif choice == '2':
                automation_repo.evaluate_rules()

            elif choice == '3':
                rule_id = int(input("Rule ID to delete: "))
                if rule_id in automation_repo.rules:
                    del automation_repo.rules[rule_id]
                    logger.log(f"Rule {rule_id} deleted")

            elif choice == '4':
                for r in automation_repo.rules:
                    print(f"Rule ID: {r}")
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            logger.log(f"Error: {e}")

def report_menu():
    print("\n-- System Report --")
    report_service.generate_report()


# === Sample Data Preload ===
user1 = UserFactory.create_user("HomeOwner", 101, "Alice")
user2 = UserFactory.create_user("Admin", 102, "Bob")
user_repo.add_user(user1)
user_repo.add_user(user2)
notification_service.subscribe(user1)
notification_service.subscribe(user2)

device1 = Device(1, "Living Room Light", "Light")
device2 = Device(2, "Main Thermostat", "Thermostat")
device3 = Device(3, "Bedroom Fan", "Fan")
device1.status = "OFF"
device2.status = "ON"
device3.status = "OFF"
device_repo.add_device(device1)
device_repo.add_device(device2)
device_repo.add_device(device3)

rule = AutomationRule(
    201,
    condition=lambda: device2.status == "ON",
    action=lambda: setattr(device2, "status", "OFF")
)
automation_repo.add_rule(rule)
# === End Sample Data ===

def main():
    while True:
        print("\n==== SMART HOME AUTOMATION SYSTEM ====")
        print("1. Device Management")
        print("2. User Management")
        print("3. Automation Rules")
        print("4. Reports")
        print("5. Exit")
        opt = input("Choose: ")

        if opt == '1':
            device_menu()
        elif opt == '2':
            user_menu()
        elif opt == '3':
            automation_menu()
        elif opt == '4':
            report_menu()
        elif opt == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()