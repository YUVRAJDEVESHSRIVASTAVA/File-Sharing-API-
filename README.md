# FileShare Django Demo

Quick start (development):

1. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run migrations and start the dev server

```bash
python manage.py migrate
python manage.py runserver
```

3. Upload and share files at http://127.0.0.1:8000/

4. Expiry job: run the management command to notify senders of unclaimed links

```bash
python manage.py expire_links
```

Expose app to the internet (shareable link)
-----------------------------------------

For quick sharing, run a tunnel tool (ngrok or localtunnel) and set the `SITE_URL` environment variable to the tunnel URL so emails contain the public link.

Examples (PowerShell):

- ngrok (if installed):
```powershell
ngrok http 8000
# copy the https://... forwarding URL shown by ngrok
$env:SITE_URL = "https://abcd1234.ngrok.io"
```

- localtunnel (requires Node.js):
```powershell
npx localtunnel --port 8000 --subdomain myfileshare
# copy the https://myfileshare.loca.lt URL and set SITE_URL
$env:SITE_URL = "https://myfileshare.loca.lt"
```

When you set `SITE_URL`, the app will use it to build share links instead of `http://127.0.0.1:8000`.

For production, deploy to a hosting platform (Render, Railway, Heroku, Azure) and set `SITE_URL` to your app's domain.


Notes:
- Email is configured to use the console backend by default (development). Configure SMTP in `fileshare_project/settings.py` for real email delivery.
- The `expire_links` command should be scheduled (cron, Task Scheduler, or a periodic worker) to run regularly.
