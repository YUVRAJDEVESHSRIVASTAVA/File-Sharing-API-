Render deployment steps

1. Connect your GitHub repo to Render (New -> Web Service -> Connect to GitHub).
2. In Render, set the build command to:

```
pip install -r requirements.txt
```

3. Set the start/command to:

```
gunicorn fileshare_project.wsgi:application --bind 0.0.0.0:$PORT
```

4. Environment variables (add in Render dashboard):
- `SECRET_KEY` — set a secure secret key
- `SITE_URL` — set to your service URL once Render gives it (e.g. https://your-app.onrender.com)
- `DEBUG` — set to `False` in production

5. Optional: enable HTTPS via Cloudflare DNS or use Render's built-in automatic TLS.

6. Static files: Render runs `collectstatic` automatically if `DISABLE_COLLECTSTATIC` is not set. Ensure `STATIC_ROOT` is present in `settings.py` (it is), and whiteNoise is configured.
