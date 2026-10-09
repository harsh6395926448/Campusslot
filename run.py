import os
from app import create_app

# Local Windows launcher: do not accidentally use a stale FLASK_ENV value.
env = os.getenv("FLASK_ENV", "development").lower()
if env not in {"development", "production"}:
    env = "development"
app = create_app(env)

if __name__ == "__main__":
    print("\nCampusSlot database:", app.config.get("SQLALCHEMY_DATABASE_URI"))
    print("CampusSlot server: http://127.0.0.1:5000")
    # 0.0.0.0 permits optional same-Wi-Fi phone testing. Cloud hosting uses Gunicorn.
    app.run(host="0.0.0.0", debug=app.config["DEBUG"], port=int(os.getenv("PORT", "5000")))
