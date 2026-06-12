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

Notes:
- Email is configured to use the console backend by default (development). Configure SMTP in `fileshare_project/settings.py` for real email delivery.
- The `expire_links` command should be scheduled (cron, Task Scheduler, or a periodic worker) to run regularly.
