# File Sharing API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Django Tests](https://github.com/YUVRAJDEVESHSRIVASTAVA/File-Sharing-API-/actions/workflows/python-tests.yml/badge.svg)](https://github.com/YUVRAJDEVESHSRIVASTAVA/File-Sharing-API-/actions/workflows/python-tests.yml)
[![Coverage](https://codecov.io/gh/YUVRAJDEVESHSRIVASTAVA/File-Sharing-API-/branch/main/graph/badge.svg?token=)](https://codecov.io/gh/YUVRAJDEVESHSRIVASTAVA/File-Sharing-API-)

Simple Django app for sharing files via expiring, tokenized links.

Features
- Upload files and generate a secure, single-use share link with expiration.
- Claim and download flow (recipient claims a file; sender is notified).
- Server-side upload validation (size + allowed extensions).
- Management command `expire_links` to cleanup expired links and delete orphaned files.
- Scheduled cleanup via GitHub Actions (cron) or host cron jobs.

Quick start (development)

Prerequisites
- Python 3.11
- Git

Local setup (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# open http://127.0.0.1:8000 to use the app
```

Run tests

```powershell
.venv\Scripts\Activate.ps1
python manage.py test
```

Configuration / environment
- `SECRET_KEY` — Django secret (set in production).
- `DEBUG` — `True` for local dev, `False` in production.
- `SITE_URL` — Public site URL used to build share links (e.g., https://example.com). If not set, links are generated from request.
- Email settings: by default the project uses the console email backend. Configure SMTP in `fileshare_project/settings.py` for production.

Deployment notes
- The repo includes a suggested `Procfile` and `gunicorn` + `whitenoise` setup for simple deployments (e.g., Render).
- For quick public exposure during development we used a Cloudflare Tunnel (cloudflared). See `docs/cloudflared-install.md` and `docs/cloudflare-dns.md`.

CI
- A GitHub Actions workflow `./.github/workflows/python-tests.yml` runs tests on push and PRs to `main`.
- The repository also contains a scheduled workflow that runs the `expire_links` management command every 10 minutes to cleanup expired links.

Security & production
- Do NOT commit secrets. Use environment variables or your host's secret store for `SECRET_KEY`, SMTP credentials, and DB credentials.
- In production consider moving files to cloud object storage (S3/GCS/Azure Blob) with signed URLs instead of serving from the web server.

Files of interest
- `sharing/` — app code (models, views, forms, templates).
- `sharing/management/commands/expire_links.py` — cleanup job.
- `.github/workflows/` — CI and scheduled jobs.
- `docs/` — documentation and deployment notes.

Contributing
- Fork, create a feature branch, add tests for new behavior, and open a PR. Tests must pass on CI.

License
- MIT (see LICENSE).

Coverage & Branch Protection
- Coverage is reported to Codecov via the `coverage.yml` workflow. If your repository is private you should set the `CODECOV_TOKEN` secret in the repository settings (`Settings -> Secrets -> Actions`) to allow uploads.
- To protect `main`, either configure branch protection rules in GitHub settings or run the manual workflow `Protect main branch` (in the Actions tab) to apply a rule that requires the `Django Tests` and `Coverage` checks and requires one approving review.

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
