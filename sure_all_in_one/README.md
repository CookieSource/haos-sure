# Sure Finance (All-in-One) for Home Assistant OS

Community prototype: Sure + PostgreSQL 16 + Redis + Sidekiq worker in ONE HAOS app.

- Only the HTTPS frontend is exposed, mapped to host port 1234 by default.
- Home Assistant ingress is enabled so the app can be shown in the sidebar.
- Database and Redis listen only on the add-on's internal loopback interface.
- Application, encryption and database secrets are generated once and stored
  in `/data/private`.
- Finance storage, database and daily PostgreSQL dumps are stored in `/data`.
- No external AI API keys or MCP endpoints are configured.
- Fresh installations only; there is no migration from a three-app install.

**Development status: UNTESTED ON A LIVE HAOS SERVER.** The YAML and shell
scripts have been statically checked, and the amd64 container has passed a
runtime smoke test outside HAOS. The first installation will compile an image
on your HAOS device and might fail if upstream Sure changes its base image or
startup expectations. Use test data first and confirm your backups.

See `DOCS.md` for installation and security details.
