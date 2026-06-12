Validation & Notifications

This document summarizes the server-side validation and notification behaviors implemented for the File Sharing API.

Validation
- Maximum upload size: `MAX_UPLOAD_SIZE` (default 50 MB). Can be overridden with the environment variable `MAX_UPLOAD_SIZE`.
- Allowed file extensions: `ALLOWED_UPLOAD_EXTENSIONS` (default includes common document/image/archive extensions). Can be overridden with the environment variable `ALLOWED_UPLOAD_EXTENSIONS` (comma-separated list, e.g. `.pdf,.png`).
- The `ShareForm` enforces both checks and returns user-friendly error messages on the UI.

Notifications & Expiry cleanup
- When a share link is created the recipient receives an email with the claim URL. Email sending uses Django's `EMAIL_BACKEND` configured in `fileshare_project/settings.py`.
- If the recipient explicitly declines and provides a reason, the sender is notified immediately with that reason.
- If a share link expires (not claimed within the configured lifetime), the `expire_links` management command performs the following for each expired link:
  - Sends a notification to the sender indicating the file was not claimed, including any reason provided by the recipient.
  - Deletes the expired `ShareLink` record so the token cannot be used.
  - If the underlying `UploadedFile` has no other active share links, the file content and its DB record are removed to free storage and protect the file.

Scheduling
- The repository includes a GitHub Actions workflow that runs `python manage.py expire_links` every 10 minutes (.github/workflows/expire_links.yml).
- For production hosts, prefer running this cleanup as a scheduled job on the host or point the workflow to the production DB via `DATABASE_URL` secret.
