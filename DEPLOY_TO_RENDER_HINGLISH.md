# CampusSlot ko Render par cloud deploy karna (Hinglish)

Is project ke liye Render web service + managed PostgreSQL configured hai. Local SQLite file cloud hosting ke liye use nahi hogi. Render ki service aur database create karne ke liye neeche ke steps follow karein.

## Deploy se pehle

- GitHub account chahiye.
- Render account chahiye.
- Gmail SMTP use kar rahe ho toh Google Account 2-Step Verification on karke 16-character App Password generate karo. Normal Gmail password kabhi use mat karo.
- `.env` file, password, app password, ya secrets GitHub par upload mat karo. `.gitignore` `.env` ko exclude karta hai.

## Step 1 — ZIP extract karo

ZIP extract karke CampusSlot project folder open karo. `render.yaml`, `requirements.txt`, `run.py`, `app/` aur `config.py` same project root mein hone chahiye.

## Step 2 — GitHub par repository banao

1. GitHub par New repository banao, e.g. `campusslot`.
2. Project files upload/push karo. `.env` ya real credentials upload na karo.
3. Check karo ki `render.yaml` repository ke root mein hai.

Agar Git use karna aata hai, project root terminal mein:

```bash
git init
git add .
git status
```

`git status` mein `.env` ya `.venv` dikhe toh commit mat karo; `.gitignore` check karo. Phir:

```bash
git commit -m "Prepare CampusSlot for cloud deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/campusslot.git
git push -u origin main
```

`YOUR-USERNAME` ko apne GitHub username se replace karo. Agar repository pehle se git repo hai, `git init`/`git remote add` dobara mat chalao.

## Step 3 — Render par deploy karo

1. Render dashboard open karo.
2. **New + → Blueprint** choose karo.
3. Apna GitHub repository connect/select karo.
4. Render `render.yaml` padhega aur CampusSlot web service + PostgreSQL database banane ke liye dikhayega.
5. Blueprint apply/deploy karo. Build logs mein error aaye toh logs ka last 30 lines save karo.

Render free-tier availability, limits, sleep/cold-start, aur database retention policy waqt ke saath badal sakte hain. Dashboard par jo current plan/retention terms dikhte hain unhe review karo; important real data ka backup rakho.

## Step 4 — Public URL verify karo

Deploy complete hone par Render web service ke page se public URL copy karo, e.g. `https://campusslot-xxxx.onrender.com`.

`config.py` automatically Render ke `RENDER_EXTERNAL_URL` ko `BASE_URL` fallback ke roop mein use karta hai. Agar tum custom domain ya alag public URL use karte ho, Render Environment mein `BASE_URL` add karo aur exact HTTPS URL set karo, trailing slash optional.

## Step 5 — Cloud admin account set karo

Render → CampusSlot web service → Environment mein ye dono variables set karo:

- `BOOTSTRAP_ADMIN_EMAIL` = jis email se admin login karna hai
- `BOOTSTRAP_ADMIN_PASSWORD` = unique password, kam se kam 12 characters

Save changes/redeploy karo. Jab cloud database naya ho aur admin table empty ho, startup par admin account create hoga. Login page: `https://YOUR-RENDER-SERVICE-URL/admin/login`. Ye environment variables tab tak delete mat karo jab tak pehla successful deploy aur admin login verify na ho jaye. Account banne ke baad password change/rotate karne ke liye app ka available admin-management workflow use karo; sirf environment variable change karne se existing admin password change nahi hota.

## Step 6 — Email settings set karo

Render → CampusSlot web service → Environment mein ye values set karo:

- `SMTP_HOST` = `smtp.gmail.com`
- `SMTP_PORT` = `587`
- `SMTP_USERNAME` = tumhara Gmail address
- `SMTP_PASSWORD` = Google ka 16-character App Password
- `MAIL_FROM` = `CampusSlot <tumhara-gmail-address>`
- `SMTP_USE_TLS` = `true`
- `SMTP_USE_SSL` = `false`

Save changes/redeploy karo. App password public repo, screenshot, ya chat mein share mat karna.

## Step 7 — Health check

Browser mein ye open karo:

`https://YOUR-RENDER-SERVICE-URL/api/advanced/health`

`YOUR-RENDER-SERVICE-URL` ko actual URL se replace karo. Healthy response aana chahiye. Agar `503` aaye toh Render logs aur `DATABASE_URL`/database status check karo.

## Step 8 — Email links mobile par test karo

1. Deployed website se naya test student ya teacher registration create karo.
2. Naya email kholo — purane emails mein localhost URL ho sakta hai.
3. Login button click karo; address bar mein deployed `https://...onrender.com` domain hona chahiye.
4. Nayi booking banao aur View Appointment link test karo.
5. Teacher action email mein Confirm/Reject/Cancel/Complete/Reschedule link kholkar confirmation page par action submit karo.
6. Dashboard aur doosre user ke notification email mein updated status verify karo.

## Important database note

Cloud database naya hai; tumhare laptop ki existing SQLite records automatically cloud mein copy nahi honge. Existing student/teacher/accounts/appointments chahiye toh migration/backup-import separately plan karo. Purane demo credentials ko assume mat karo; admin access aur user accounts ko deployment ke baad verify karo.

## Troubleshooting

- **Build fails on psycopg2:** confirm `psycopg2-binary` is present in `requirements.txt` and redeploy.
- **Health check fails:** Render logs dekho; database service running hai aur `DATABASE_URL` web service se linked hai ye verify karo.
- **Email links localhost par jaate hain:** Render Environment mein `BASE_URL` ko exact deployed HTTPS URL set karo; service redeploy/restart karo aur fresh email generate karo.
- **Emails nahi aate:** SMTP settings, Gmail App Password, sender address, aur Render logs check karo.
- **Buttons link open karte hain par action fail hota hai:** action page par message aur server logs check karo; expired/signed action links ko fresh email se test karo.
- **Database error after deploy:** deployment logs share karo, secrets/passwords redact karke. Production database ko delete/reset mat karo.

## Local development ab bhi kaam karega

Windows local setup ke liye `START_HERE_WINDOWS.txt` follow karo. Local development SQLite use kar sakta hai; cloud production PostgreSQL use karta hai.
