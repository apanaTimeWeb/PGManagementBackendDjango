import pytest
import requests
import os
import django

# Setup Django manually to access Real DB
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pgmanagement.settings')
django.setup()

from apps.users.models import CustomUser

class TestLoginAPI:
    def setup_method(self):
        self.login_url = "http://127.0.0.1:8000/api/v1/auth/login/"
        self.user_data = {
            "username": "test_login_real_user",
            "email": "test_login_real@example.com",
            "phone_number": "9988776655",
            "password": "StrongPassword123!",
            "role": "TENANT"
        }
        
        # Ensure clean state first
        self.cleanup_user()

        # Create user in REAL DB for login test
        user, created = CustomUser.objects.get_or_create(
            username=self.user_data["username"],
            email=self.user_data["email"],
            phone_number=self.user_data["phone_number"],
            defaults={"role": self.user_data["role"]}
        )
        user.set_password(self.user_data["password"])
        user.save()

    def cleanup_user(self):
        # Cleanup
        try:
            user = CustomUser.objects.filter(username=self.user_data["username"]).first()
            if user:
                user.delete()
                print(f"\n[Cleanup] Deleted user: {self.user_data['username']}")
        except Exception as e:
            print(f"\n[Cleanup Error]: {e}")

    def teardown_method(self):
        self.cleanup_user()

    def test_login_success(self):
        """
        Test valid login against LIVE server.
        """
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }
        response = requests.post(self.login_url, json=data)
        assert response.status_code == 200
        json_data = response.json()
        assert "access" in json_data
        assert "refresh" in json_data

    def test_login_invalid_credentials(self):
        data = {
            "username": self.user_data["username"],
            "password": "WrongPassword"
        }
        response = requests.post(self.login_url, json=data)
        assert response.status_code == 401
