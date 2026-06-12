Cloudflare DNS and proxy guide

1. Add your domain to Cloudflare and update your registrar's nameservers to the ones Cloudflare provides.
2. In the Cloudflare dashboard -> DNS, add a record pointing your domain to the host:
   - If your host provides a CNAME target (e.g., `your-app.onrender.com`), add a `CNAME` record for `www` pointing to that target and enable the proxy (orange cloud).
   - For root domains without CNAME support, add an `A` record to the host IP and enable proxying.
3. In Cloudflare -> SSL/TLS, set mode to `Full (strict)` if you have valid certs on the origin, otherwise `Full`.
4. (Optional) Add Page Rules or Transform Rules for caching, redirects, or security headers.
5. If you use Cloudflare Tunnel (cloudflared) for ephemeral exposure, run `cloudflared tunnel --url http://127.0.0.1:8000` and use the returned `trycloudflare.com` URL.

Notes:
- When proxying via Cloudflare, the hostname seen by the origin will be `127.0.0.1:8000` for local tunnels or the host's IP for deployed services. Ensure `ALLOWED_HOSTS` in Django allows your domain.
- For production, set `SITE_URL` to your domain (e.g., https://files.example.com) so share emails use the correct domain.
