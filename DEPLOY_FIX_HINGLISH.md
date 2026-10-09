# CampusSlot Cloud Deployment Fix (Beginner Hinglish)

## Why the previous deployment failed

Render logs showed `ModuleNotFoundError: No module named 'app'` while importing `run.py`.
This package contains the required `app/` Python package. The GitHub repository used by Render must contain that folder at the repository root, next to `run.py` and `render.yaml`.

## IMPORTANT: Preserve folders when updating GitHub

Do not upload only the top-level files using GitHub's web upload screen. The `app/` folder contains routes, models, templates, and services required by the application.

### Recommended Windows method (GitHub Desktop)
1. Download and extract `CampusSlot-CLOUD-DEPLOY-FIXED.zip`.
2. Install/open GitHub Desktop: https://desktop.github.com/
3. Clone your existing repository `harsh6395926448/Campusslot` to your computer.
4. Open the cloned repository folder in File Explorer.
5. Copy **all files and folders from the extracted ZIP** into the cloned repository folder. Allow overwrite when asked. Copy the `app` folder itself, not only the files inside it.
6. Confirm the cloned repository root contains all of these:
   - `app/` (folder, with `__init__.py`, `routes/`, `models/`, `templates/`, `services/`)
   - `run.py`
   - `config.py`
   - `requirements.txt`
   - `render.yaml`
   - `.python-version`
7. In GitHub Desktop, review the changed files, enter a summary such as `Restore full CampusSlot package for Render`, click **Commit to main**, then **Push origin**.
8. Return to Render. The Blueprint should sync from the new commit and redeploy the service.

## Render configuration

The repository `render.yaml` sets the production command to:

`gunicorn run:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`

The `.python-version` file pins Python to 3.12.10 to avoid unexpectedly selecting a newer runtime.

Blueprint-managed resources:
- Web service: `campusslot`
- PostgreSQL database: `campusslot-db`

Do not delete the existing database to fix a missing Python package.

## Environment variables

The Blueprint asks for the following values:
- `BOOTSTRAP_ADMIN_EMAIL`: a real email address you control (this is the admin login name)
- `BOOTSTRAP_ADMIN_PASSWORD`: a unique password of at least 12 characters; do not reuse your Gmail password
- `SMTP_HOST`: `smtp.gmail.com`
- `SMTP_USERNAME`: your Gmail address
- `SMTP_PASSWORD`: a Google App Password, not your normal Gmail password
- `MAIL_FROM`: your sender address, usually the same Gmail address

`SMTP_PORT`, `SMTP_USE_TLS`, `SECRET_KEY`, `ADMIN_SECRET_KEY`, and `DATABASE_URL` are configured by the Blueprint unless you deliberately change them. Never put `.env` or real secrets in GitHub.

## Verify after deploy

1. Wait until Render says the web service is **Live**.
2. Open `https://YOUR-SERVICE.onrender.com/api/advanced/health`.
3. Expected response includes `"status":"healthy"` and `"database":"postgresql"`.
4. Test student/teacher login, a new booking, teacher confirmation/rejection/rescheduling, and the resulting email buttons using newly generated emails.

## Honest verification note

This ZIP's Python files compile and the included email-link tests pass in the packaging environment. A live Render deployment and live Gmail delivery cannot be verified from this local packaging step. If Render still fails, use its newest deployment logs; do not delete the database or randomly change secrets.
