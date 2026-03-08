import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safelogin.settings')
django.setup()

from auth_app.models import User
from django.contrib.auth import authenticate

# Create a test user for login testing
username = "testuser2"
password_wrong = "wrongpassword"

# Delete existing test user if any
User.objects.filter(username=username).delete()

# Create a fresh test user
user = User.objects.create_user(username=username, email="test2@test.com", password="correctpassword")
print(f"✓ Created test user: {username}")
print(f"✓ Correct password: correctpassword")
print(f"✓ We will attempt login with WRONG password: {password_wrong}")

# Simulate a failed login attempt (same as login_view does)
print("\n--- Attempting failed login ---")
result = authenticate(username=username, password=password_wrong)
if result is None:
    print("✓ Authentication failed (as expected)")
    
    # Now manually log the failed attempt like the view does
    logger = logging.getLogger("auth_app")
    logger.warning(f"Failed login attempt for user: {username} from IP: 127.0.0.1")
    print("✓ Logger.warning() called")

# Check log file
log_path = os.path.join(os.path.dirname(__file__), "logs", "security.log")
print(f"\n--- Checking log file at: {log_path} ---")
if os.path.exists(log_path):
    with open(log_path, 'r') as f:
        content = f.read()
        lines = content.strip().split('\n')
        print(f"✓ Log file has {len(lines)} entries:")
        for line in lines[-5:]:  # Show last 5 entries
            print(f"  - {line}")
else:
    print(f"✗ Log file not found!")
