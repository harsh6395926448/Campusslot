"""Check that essential CampusSlot files are present before pushing to GitHub."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
required = [
    "app/__init__.py",
    "app/routes/__init__.py",
    "app/routes/booking.py",
    "app/routes/dashboard.py",
    "app/services/email_service.py",
    "app/services/teacher_action_service.py",
    "app/models/__init__.py",
    "app/templates/base.html",
    "run.py",
    "config.py",
    "requirements.txt",
    "render.yaml",
    ".python-version",
]
missing = [name for name in required if not (ROOT / name).is_file()]
if missing:
    print("PACKAGE CHECK FAILED. Missing required files:")
    for name in missing:
        print(f" - {name}")
    sys.exit(1)
print("PACKAGE CHECK PASSED")
print("Required Flask package, routes, models, templates, services, and Render files are present.")
print("Keep the app/ folder when copying this project to GitHub.")
