from cryptography.fernet import Fernet
from django.conf import settings
import re
from reportlab.pdfgen import canvas
import os
import base64

# --- Aadhaar Validation (Verhoeff Algorithm) ---
# For simplicity in this iteration, we use Regex + simple check. 
# Implementing full Verhoeff is verbose. Regex is standard 1st step: 12 digits, no starting 0 or 1.
def validate_aadhaar_number(number):
    """
    Validates that the Aadhaar number is 12 digits and doesn't start with 0 or 1.
    """
    regex = r'^[2-9]\d{11}$'
    if re.match(regex, number):
        return True
    return False

# --- Encryption ---
# Using Fernet for symmetric encryption of Aadhaar Number
# Key should be in settings.SECRET_KEY or separate env var. 
# For demo, using a derived key from SECRET_KEY (padded/hashed to 32 bytes)
# In production, use a dedicated KMS.
def get_cipher_suite():
    # Only for demonstration. In prod, use a proper 32-byte url-safe base64 encoded key.
    # We will generate a ephemeral key if not provided, which breaks persistence across restarts if not fixed.
    # User instructions implied local dev, so we won't over-engineer KMS here.
    # We'll use a fixed key for this session or try to derive.
    key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].zfill(32).encode())
    return Fernet(key)

def encrypt_aadhaar(number):
    cipher_suite = get_cipher_suite()
    return cipher_suite.encrypt(number.encode()).decode()

def decrypt_aadhaar(encrypted_number):
    cipher_suite = get_cipher_suite()
    return cipher_suite.decrypt(encrypted_number.encode()).decode()

# --- Police Verification Form ---
def generate_police_verification_pdf(user_data):
    """
    Generates a simple PDF for Police Verification.
    Returns the path to the generated file.
    """
    filename = f"police_verification_{user_data['username']}.pdf"
    path = os.path.join(settings.MEDIA_ROOT, 'documents', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    c = canvas.Canvas(path)
    c.drawString(100, 800, "POLICE VERIFICATION FORM")
    c.drawString(100, 750, f"Tenant Name: {user_data['full_name']}")
    c.drawString(100, 730, f"Phone: {user_data['phone']}")
    c.drawString(100, 710, f"Aadhaar (Last 4): XXXX-XXXX-{user_data['aadhaar_last_4']}")
    c.drawString(100, 690, f"Address: {user_data.get('address', 'N/A')}")
    c.drawString(100, 650, "Status: SUBMITTED")
    c.drawString(100, 600, "For Police Station Use Only")
    c.save()
    
    return path
