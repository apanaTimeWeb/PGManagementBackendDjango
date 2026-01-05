import pytest
import requests
import os
import django

# Setup Django manually to access Real DB for cleanup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pgmanagement.settings')
django.setup()

from apps.users.models import CustomUser

class TestRegisterAPI:
    def setup_method(self):
        self.base_url = "http://127.0.0.1:8000/api/v1/auth/register/"
        self.user_data = {
            "username": "test_real_db_user",
            "email": "test_real@example.com",
            "phone_number": "1122334455",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
            "role": "TENANT"
        }

            "role": "TENANT"
        }
        # Ensure clean state before starting any test
        self.cleanup_user()

    def cleanup_user(self):
        # Cleanup: Delete the user from REAL database
        try:
            user = CustomUser.objects.filter(username=self.user_data["username"]).first()
            if user:
                user.delete()
                print(f"\n[Cleanup] Deleted user: {self.user_data['username']}")
        except Exception as e:
            print(f"\n[Cleanup Error]: {e}")

    def teardown_method(self):
        self.cleanup_user()

    def test_register_user_success(self):
        """
        Test valid user registration against LIVE server.
        """
        response = requests.post(self.base_url, json=self.user_data)
        assert response.status_code == 201
        
        # Verify in DB
        assert CustomUser.objects.filter(username=self.user_data["username"]).exists()

    def test_register_duplicate_user(self):
        """
        Test that registering a duplicate user fails.
        """
        # 1. Register first time
        requests.post(self.base_url, json=self.user_data)
        
        # 2. Register again
        response = requests.post(self.base_url, json=self.user_data)
        assert response.status_code == 400
