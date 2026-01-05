import os
import django
import sys
import time

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pgmanagement.settings')
django.setup()

from django.test import RequestFactory
from apps.users.views.auth_views import LoginView
from apps.users.models import CustomUser, ActivityLog
from rest_framework.test import APIRequestFactory
from django.core.cache import cache

def run_verification():
    print("--- Starting Login Verification ---")
    
    # 1. Setup Test User
    username = "test_login_user"
    password = "SafePassword123!"
    email = "test_login@example.com"
    
    user, created = CustomUser.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
        print(f"[Setup] Created test user: {username}")
    else:
        user.set_password(password) # Ensure password is known
        user.save()
        print(f"[Setup] Reset password for existing user: {username}")

    # Clear cache for clean slate
    cache.clear()

    factory = APIRequestFactory()
    view = LoginView.as_view()

    # 2. Test Success
    print("\n[Test 1] Testing Successful Login...")
    data = {"username": username, "password": password}
    request = factory.post('/api/v1/auth/login/', data, format='json')
    response = view(request)
    
    if response.status_code == 200 and 'access' in response.data:
        print("✅ SUCCESS: Login successful, token received.")
    else:
        print(f"❌ FAILED: Start Code {response.status_code}, Data: {response.data}")

    # 3. Test Failure (Wrong Password)
    print("\n[Test 2] Testing Invalid Credentials...")
    data_wrong = {"username": username, "password": "WrongPassword"}
    request = factory.post('/api/v1/auth/login/', data_wrong, format='json')
    response = view(request)
    
    if response.status_code == 401:
        print("✅ SUCCESS: Correctly rejected invalid credentials.")
    else:
        print(f"❌ FAILED: Expected 401, got {response.status_code}")

    # 4. Test Rate Limiting
    print("\n[Test 3] Testing Rate Limiting (this might take a few seconds)...")
    # We already failed once. Let's fail 5 more times to trigger lockout (Total 6)
    # Note: Our limit is 5 failed attempts -> Lockout.
    # We did 1 fail above.
    
    for i in range(5):
        request = factory.post('/api/v1/auth/login/', data_wrong, format='json')
        response = view(request)
        if response.status_code == 429:
            print(f"✅ SUCCESS: Rate limit triggered on attempt {i+2}")
            break
        elif response.status_code == 401:
             print(f"Attempt {i+2}: Failed as expected (401)")
    else:
        print("❌ FAILED: Rate limit NOT triggered after 6 attempts.")

    # 5. Verify Logging
    print("\n[Test 4] Verifying Activity Log...")
    log = ActivityLog.objects.filter(user=user, action="USER_LOGIN").last()
    if log:
        print(f"✅ SUCCESS: Log found: {log.details} at {log.timestamp}")
    else:
        print("❌ FAILED: No login activity log found.")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    run_verification()
