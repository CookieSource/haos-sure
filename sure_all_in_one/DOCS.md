# Sure Finance All-in-One - documentation

## Prerequisites

- Home Assistant OS on x86_64 (amd64), with sufficient disk space for Docker
  image building, PostgreSQL and Redis.
- Internet access from HAOS to public images and package repositories at build time.
- A trusted TLS certificate and key in Home Assistant's `/ssl` directory. The
  defaults are `/ssl/fullchain.pem` and `/ssl/privkey.pem`.
- The container has been runtime smoke-tested on amd64, but not yet inside
  Home Assistant OS. Use test data first.

## Install

Copy the `sure_all_in_one` folder into Home Assistant's `/local_apps/`
folder (through Terminal & SSH or Samba). In Home Assistant go to
**Settings > Apps > App Store > menu > Check for updates / Reload**, find
**Sure Finance (All-in-One)** under **Local apps**, and install it.

Alternative: publish this whole repository to a Git repository and add that
repository URL under App Store > Repositories. Local installation does not
require publishing the code.

Sure will build on your Home Assistant OS device. Start the app and use
**Open Web UI**, or open **https://<your-ha-host>:1234**. Database and Redis are
started automatically inside the same app. The certificate must be trusted by
the browser and its hostname must match the URL you use.

To add Sure to the Home Assistant sidebar, open the installed app's page and
enable **Show in sidebar**. The sidebar uses Home Assistant ingress while the
direct HTTPS address on port 1234 remains available.

The `ssl` option defaults to `true`. `certfile` and `keyfile` are filenames
inside Home Assistant's `/ssl` directory. Disabling `ssl` is intended only for
local troubleshooting; bank authorization providers generally require a
stable HTTPS callback URL with a publicly trusted certificate.

### Enable Banking callback without a public port

Set `enable_banking_callback_url` when Sure is accessed through Home Assistant
ingress or when the hostname visible to Sure is not the hostname registered
with Enable Banking. Leave it blank to retain Sure's normal request-derived
callback. A configured value must be the complete HTTPS URL, for example:

```text
https://sure.example.com/enable_banking_items/callback
```

For a LAN/VPN-only callback without router port forwarding:

1. Use a real domain that you control.
2. Obtain a publicly trusted certificate with DNS validation and place its
   certificate/key in Home Assistant's `/ssl` directory.
3. Configure local or VPN DNS so the hostname resolves to the Home Assistant
   LAN address only for your devices.
4. Serve that hostname locally over HTTPS. Using local port 443 through a
   reverse proxy avoids a nonstandard port; otherwise include the mapped port
   in the callback URL.
5. Enter the exact URL above in both this app setting and the Enable Banking
   application settings.
6. Complete authorization in the same browser while connected to that LAN/VPN.

This setting changes only the URL Sure displays and submits to Enable Banking.
It does not create DNS records, obtain a certificate, configure a reverse
proxy, or expose a port. Some banks may impose additional requirements.

## First login and safety

1. Create your account using test data first.
2. Immediately change the app option `onboarding_state` from `open` to
   `closed` and restart the app to prevent more signups.
3. Expose port 1234 only when a bank authorization callback requires it, and
   restrict access with your firewall or trusted reverse proxy.
4. Use a stable HTTPS hostname with a trusted certificate for sensitive data
   and bank authorization callbacks.
5. Do not configure Sure's optional OpenAI/Anthropic integrations or install
   financial Home Assistant sensors/MCP tools. This package clears common AI
   environment credentials and opts out of PostHog feedback, but upstream
   features can change and this is not a formal data-leak prevention boundary.
6. HA administrative MCP access can still affect add-on management. The only
   strict way to prevent access from a privileged AI agent is separate
   infrastructure and access controls.
7. For automatic Revolut syncing, Sure requires Enable Banking authorization.
   Enable Banking is a third-party financial data processor, not an AI service.

## Data and backup

Everything is under Home Assistant's persistent app `/data` folder:

- `/data/postgres` - PostgreSQL 16 database.
- `/data/redis` - Redis append-only data.
- `/data/storage` - uploaded files and user data.
- `/data/private/sure-secrets.env` - generated application, database and
  encryption secrets.
- `/data/backups` - rotating daily PostgreSQL dumps (7-day retention).

Back up the entire add-on including `/data`, not merely the database dumps.
Use encrypted backups outside the Home Assistant machine. **Never regenerate
or edit `sure-secrets.env`:** it contains `SECRET_KEY_BASE` and the three
Active Record encryption keys used to protect sensitive data. Losing or
changing these values can make encrypted data unreadable.

Do not replace PostgreSQL 16 with a different major version in the image
without a proper database dump and restore migration.

## Limitations

- Built and smoke-tested as an amd64 container; not yet tested on HAOS itself.
- Runs several services in one container (web, worker, PostgreSQL, Redis).
- Updates require an intentional rebuild/test and app version increase; the
  upstream `stable` tag can change, so test releases before real use.
- This is not an official Sure release and is not endorsed by Home Assistant.
- HTTPS is enabled by default; keep certificates current and do not downgrade
  to HTTP when entering sensitive account details or bank credentials.
