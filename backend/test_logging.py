import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safelogin.settings')
django.setup()

from auth_app.models import User

# Test the logger
logger = logging.getLogger("auth_app")
logger.warning("Failed login attempt for user: testuser from IP: 192.168.1.1")
logger.warning("Another test warning message")
print("Logger warnings sent")

# Check if log file was created
log_path = os.path.join(os.path.dirname(__file__), "logs", "security.log")
if os.path.exists(log_path):
    with open(log_path, 'r') as f:
        content = f.read()
        print(f"\n=== Log file content ({log_path}) ===")
        print(content)
        print("=== End of log ===\n")
else:
    print(f"Log file not found at: {log_path}")
    print(f"Checking if logs directory exists: {os.path.exists(os.path.dirname(log_path))}")
