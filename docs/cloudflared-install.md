Installing cloudflared (Windows)

1. Download the official installer (MSI) from Cloudflare:
   - Visit: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   - Under Windows, download the `.msi` installer and run it.

2. Verify installation in PowerShell:
```
cloudflared --version
```

3. If you prefer package managers:
- Winget (may not have the package in all regions):
```
winget install --id Cloudflare.Cloudflared -e --accept-package-agreements --accept-source-agreements
```
- Chocolatey:
```
choco install cloudflared
```

4. Start an ephemeral tunnel pointing to your local dev server:
```
cloudflared tunnel --url http://127.0.0.1:8000
# cloudflared will print a public https://...trycloudflare.com URL
```

5. Set `SITE_URL` in your PowerShell session (so emails use the public URL):
```
$env:SITE_URL = "https://<your-trycloudflare-id>.trycloudflare.com"
# then restart Django runserver in same shell
.venv\Scripts\python manage.py runserver 127.0.0.1:8000
```

Notes:
- For persistent usage, consider installing cloudflared as a service and creating a named tunnel with a CNAME to `trycloudflare` or using Cloudflare for Teams for longer-lived tunnels.
