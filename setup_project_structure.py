
import os
import sys

PROJECT_ROOT = "/home/satyamambani/Desktop/project_to_work/PGManagementBackendDjango"

STRUCTURE = {
    "": [
        ".env",
        ".gitignore",
        "requirements.txt",
        "manage.py",
        "docker-compose.yml",
        "Dockerfile",
        "README.md",
    ],
    "core": [
        "__init__.py",
        "urls.py",
        "wsgi.py",
        "asgi.py",
    ],
    "core/settings": [
        "__init__.py",
        "base.py",
        "development.py",
        "production.py",
        "testing.py",
    ],
    "shared": [
        "__init__.py",
        "permissions.py",
    ],
    "shared/middleware": [
        "error_handling.py",
        "request_logging.py",
        "cors_middleware.py",
    ],
    "shared/utils": [
        "api_response.py",
        "file_upload.py",
        "pdf_generator.py",
        "sms_utils.py",
        "translation.py",
    ],
    "shared/localization": [
        "middleware.py",
        "language_loader.py",
    ],
    "apps": [], # Parent folder
    # Apps will be generated in a loop to avoid repetition, but some have specific sub-files
    "media": [],
    "static": [],
}

APPS = [
    "users",
    "properties",
    "bookings",
    "finance",
    "operations",
    "mess",
    "crm",
    "notifications",
    "visitors",
    "inventory",
    "payroll",
    "hygiene",
    "feedback",
    "audit",
    "alumni",
    "saas",
    "reports",
    "localization",
]

# Specific app structures based on docs
APP_STRUCTURES = {
    "users": {
        "models": ["user.py", "tenant_profile.py", "staff_profile.py"],
        "serializers": [], "views": [], "services": [], "tests": []
    },
    "properties": {
        "models": ["property.py", "room.py", "bed.py", "asset.py", "pricing.py"],
        "services": ["dynamic_pricing.py", "iot_integration.py"]
    },
    "bookings": {
        "models": ["booking.py", "agreement.py"],
        "services": ["allocation.py", "agreement_gen.py"]
    },
    "finance": {
        "models": ["invoice.py", "transaction.py", "expense.py"],
        "services": ["invoice_generator.py", "wallet_manager.py"]
    },
    "operations": {
        "models": ["complaint.py", "entry_log.py", "notice.py", "chat_log.py"],
        "services": ["chatbot_logic.py", "complaint_router.py"]
    },
    "mess": {
        "models": ["menu.py", "selection.py"],
        "services": ["meal_billing.py"]
    },
    "crm": {"models": [], "serializers": [], "views": []}, # Simplified in docs
    "notifications": {"models": [], "services": ["dispatcher.py"]},
    "visitors": {"models": [], "views": []},
    "inventory": {"models": [], "views": []},
    "payroll": {
        "models": [], "services": ["salary_calc.py"]
    },
    "hygiene": {"models": [], "views": []},
    "feedback": {"models": []},
    "audit": {
        "models": [], "middleware": ["audit_middleware.py"]
    },
    "alumni": {"models": []},
    "saas": {"models": []},
    "reports": {
        "services": ["excel_export.py", "chart_data.py"], "views": []
    },
    "localization": {
        "models": [], "serializers": [], "views": [],
        "services": ["translation_manager.py", "language_detector.py"],
        "management/commands": ["load_translations.py"]
    }
}


def create_structure():
    print(f"Creating project structure in {PROJECT_ROOT}...")
    
    # Create base paths
    for path, files in STRUCTURE.items():
        full_path = os.path.join(PROJECT_ROOT, path)
        os.makedirs(full_path, exist_ok=True)
        for f in files:
            file_path = os.path.join(full_path, f)
            if not os.path.exists(file_path):
                print(f"Creating {file_path}")
                try:
                    with open(file_path, 'w') as file:
                        pass # Create empty file
                except Exception as e:
                    print(f"Error creating {file_path}: {e}")

    # Create Apps
    apps_dir = os.path.join(PROJECT_ROOT, "apps")
    os.makedirs(apps_dir, exist_ok=True)
    
    for app in APPS:
        app_path = os.path.join(apps_dir, app)
        os.makedirs(app_path, exist_ok=True)
        
        # Default subfolders for all apps (unless specified otherwise, but good to have)
        # Docs show mix, but generally models/urls.py etc are standard.
        # We will follow specific APP_STRUCTURES but add generic urls.py if not mentioned implicitly (docs say urls.py for all)
        
        # Always create urls.py for every app
        open(os.path.join(app_path, "urls.py"), 'a').close()
        open(os.path.join(app_path, "__init__.py"), 'a').close()

        specifics = APP_STRUCTURES.get(app, {})
        
        # If specifics has 'models' key that is a list, it means models folder. 
        # If keys are missing (like views), docs imply simple struct or handled in standard way.
        # I'll default to creating standard folders if not explicitly forbidden, but prioritising doc specs.
        
        # Standard folders to checking docs against or default to:
        # Docs show 'models.py' for some (crm), 'models/' folder for others (users).
        # Wait, docs say:
        # crm: models.py (file)
        # users: models/ (dir)
        # I need to distinguish.
        
        # Re-reading docs structure carefully in my code logic:
        # "models/" implies directory.
        # "models.py" in docs implies file.
        # My APP_STRUCTURES dict above uses 'models' as key for a LIST of files. 
        # If 'models' key exists and is list, I create basic folder.
        # BUT for crm, docs said "models.py".
        # Let's adjust logic.
        
        # Actually docs say:
        # apps/users/models/ -> user.py etc.
        # apps/crm/models.py
        
        # I need to handle this.
        # Check APP_STRUCTURES again. 
        # crm maps to {"models": [], ...} in my set above. 
        # I will modify APP_STRUCTURES below in execution to match docs precisely.
        pass

    # Refined App Processing
    for app in APPS:
        app_path = os.path.join(apps_dir, app)
        
        # default urls.py and __init__.py
        with open(os.path.join(app_path, "urls.py"), 'a') as f: pass
        with open(os.path.join(app_path, "__init__.py"), 'a') as f: pass

        details = APP_STRUCTURES.get(app, {})
        
        # Check if we should use models MODULE or models FILE
        # Hueristic: If 'models' in details has list of files, it's a module.
        # If 'models' is NOT in details, or empty list? 
        # Wait, for 'crm', docs say 'models.py'. My dict had empty list.
        # Let's hardcode the 'folder' vs 'file' distinction based on docs.
        
        uses_models_folder = app in [
            "users", "properties", "bookings", "finance", "operations", "mess"
        ]
        
        if uses_models_folder:
            # Create models/ folder
            m_path = os.path.join(app_path, "models")
            os.makedirs(m_path, exist_ok=True)
            with open(os.path.join(m_path, "__init__.py"), 'a') as f: pass
            
            # Create specific model files
            for m_file in details.get("models", []):
                with open(os.path.join(m_path, m_file), 'a') as f: pass
        else:
            # Create models.py
            with open(os.path.join(app_path, "models.py"), 'a') as f: pass

        # Handle other keys in details (services, views, serializers, middleware, management)
        for key, items in details.items():
            if key == "models": continue # Handled above
            
            # If key is path like "management/commands"
            subpath = os.path.join(app_path, key)
            os.makedirs(subpath, exist_ok=True)
            with open(os.path.join(subpath, "__init__.py"), 'a') as f: pass
            
            for item in items:
                with open(os.path.join(subpath, item), 'a') as f: pass
                
        # For apps that didn't have specific services/views in 'details' but might need them?
        # Docs say:
        # crm: serializers.py, views.py
        # visitors: views.py
        # inventory: views.py
        # hygiene: views.py
        # reports: views.py
        # localization: serializers.py, views.py
        
        # I will cover these explicitly
        if app == "crm":
             with open(os.path.join(app_path, "serializers.py"), 'a') as f: pass
             with open(os.path.join(app_path, "views.py"), 'a') as f: pass
        
        if app in ["visitors", "inventory", "hygiene", "reports", "localization"]:
             with open(os.path.join(app_path, "views.py"), 'a') as f: pass
             
        if app == "localization":
             with open(os.path.join(app_path, "serializers.py"), 'a') as f: pass

if __name__ == "__main__":
    if "--verify" in sys.argv:
        # Verification logic
        missing = []
        # Re-check core struct
        for path, files in STRUCTURE.items():
            full_path = os.path.join(PROJECT_ROOT, path)
            for f in files:
                if not os.path.exists(os.path.join(full_path, f)):
                    missing.append(os.path.join(path, f))
        
        if missing:
            print("Missing files:")
            for m in missing:
                print(f"- {m}")
        else:
            print("Verification Successful: Base structure exists.")
    else:
        create_structure()
