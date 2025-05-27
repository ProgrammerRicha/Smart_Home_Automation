# Smart Home Automation System (Console-Based)

## Overview
This Python-based console application simulates a Smart Home Automation System with a modular and design-pattern-rich architecture.

### Features
- **Device Management**: Add, update, delete, view smart devices.
- **User Management**: Register, delete, and manage user roles (Admin/Homeowner).
- **Automation Rules**: Create and evaluate automation based on device status.
- **Notifications**: Notify users via console using Publish-Subscribe pattern.
- **Reports**: Generate device, user, and automation reports.

## Design Patterns Used
- **Singleton**: Logger
- **Factory Method**: User roles
- **Publish-Subscribe**: Notification system
- **Lazy Loading**: Device status
- **Repository**: Device/User/Automation Rule storage abstraction
- **Interceptor**: Request logging
- **Microservices Decomposition**: Modular services structure

##  File Structure
```
smart_home_automation/
├── main.py
└── README.md
```

##  How to Run
1. **Ensure Python 3.7+ is installed.**
2. **Navigate to the project folder in your terminal.**
3. **Run the program:**
```bash
python main.py
```

## Notes
- No database or third-party packages used.
- Pure Python 3 standard library.
- Focus on SOLID principles and extensible architecture.

## Sample Output
```
==== SMART HOME AUTOMATION SYSTEM STARTED ====
[LOG]: Pre-processing Add Device
[LOG]: Device Living Room Light added
...
[HomeOwner - Alice]: Device Living Room Light updated: {'status': 'ON'}
...
[LOG]: Report generated
==== SMART HOME AUTOMATION SYSTEM ENDED ====
```
