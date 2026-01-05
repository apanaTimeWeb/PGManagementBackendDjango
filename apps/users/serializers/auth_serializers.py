from rest_framework import serializers  # Importing DRF serializers to handle data validation and conversion
from django.contrib.auth.password_validation import validate_password  # Importing Django's built-in password validation (length, complexity)
from apps.users.models import CustomUser  # Importing the CustomUser model where user data will be stored

# Serializer class for User Registration, inherits from ModelSerializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    # Field for password input: Validated for complexity, write-only (never returned in response), required
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    # Field for confirming password: write-only, required to ensure user didn't make a typo
    confirm_password = serializers.CharField(write_only=True, required=True)

    # Meta class provides metadata about the serializer
    class Meta:
        model = CustomUser  # The model this serializer is linked to
        # List of fields that should be included in the API input/output
        fields = ['username', 'email', 'phone_number', 'password', 'confirm_password', 'role']

    # Custom validation method for the entire object
    def validate(self, attrs):
        # Check if the 'password' and 'confirm_password' fields match
        if attrs['password'] != attrs['confirm_password']:
            # If they don't match, raise a validation error
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # If valid, return the dictionary of validated attributes
        return attrs

    # Method to create a new user instance
    def create(self, validated_data):
        # Remove 'confirm_password' from the data dictionary as it's not a model field
        validated_data.pop('confirm_password')
        
        # Use Django's create_user method which handles password hashing automatically
        user = CustomUser.objects.create_user(**validated_data)
        
        # Return the created user instance
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

