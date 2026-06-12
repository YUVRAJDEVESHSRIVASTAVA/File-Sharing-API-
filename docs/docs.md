Project plan and developer notes (7-day breakdown)

Day 1 — Setup storage & project scaffold
- Create Django project and `sharing` app.
- Configure `MEDIA_ROOT` and `MEDIA_URL` for uploads (see [fileshare_project/settings.py](fileshare_project/settings.py#L1)).
- Add `UploadedFile` and `ShareLink` models to store uploaded files and share tokens ([sharing/models.py](sharing/models.py#L1)).

Day 2 — Upload API + UI
- Single upload form (`ShareForm`) accepts `file`, `sender_email`, and `recipient_email` ([sharing/forms.py](sharing/forms.py#L1)).
- The view `index` saves the file and creates a `ShareLink` with a 30-minute expiry ([sharing/views.py](sharing/views.py#L1)).
- Simple, clean UI is implemented with Bootstrap in templates under [sharing/templates/sharing](sharing/templates/sharing).

Day 3 — Download API + claim flow
- `claim_view` shows file info and a button to claim and download.
- Claiming sets `claimed=True` and records `claimed_at`. The file is returned via `FileResponse` in `download_view`.

Day 4 — Share link generation
- A tokenized link is generated and emailed to the recipient. The sender receives a confirmation when the file is claimed.

Day 5 — Expiry logic & cleanup job
- `ShareLink` expires after 30 minutes. A management command `expire_links` marks expired links and emails the sender with any provided decline reason ([sharing/management/commands/expire_links.py](sharing/management/commands/expire_links.py)).

Day 6 — Validation & notifications
- Recipient can optionally decline and provide a reason. That reason is included when notifying the sender.
- Email uses Django's console backend by default — configure SMTP for production in `fileshare_project/settings.py`.

Day 7 — Testing & docs
- Add tests and validate flows (not included in this scaffold but straightforward to add with Django's test client).
- This document explains where each piece lives and how to run the expiry notification.

Running Tests
- **Local:** create and activate your virtualenv, install dependencies, then run:

	python -m venv .venv
	.venv\Scripts\Activate.ps1  # PowerShell on Windows
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py test

- **CI:** A GitHub Actions workflow `python-tests.yml` (in `.github/workflows/`) runs tests on push and pull requests to `main`. It sets up Python 3.11, installs dependencies, runs migrations, and executes `manage.py test`.

Security and UX notes:
- Tokens are unguessable (`secrets.token_urlsafe`) and tied to a file record.
- Files are served only through the claim/download flow — direct access requires knowledge of media URL and path; in production, use private storage or signed URLs.
- The UI is intentionally minimal: a single page to upload and share, a clear claim page, and concise messages.
