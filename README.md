# Sure Finance All-in-One HAOS app repository

This project packages four services into one installable Home Assistant OS app:

- Sure Finance (upstream image `ghcr.io/we-promise/sure:stable`)
- PostgreSQL 16
- Redis
- Background Sidekiq worker

It is a local, source-built package for amd64 HAOS, not a prebuilt image.

## Quick install (no GitHub required)

1. Extract the ZIP file.
2. Copy the **sure_all_in_one** directory to Home Assistant's
   `/local_apps/sure_all_in_one` using Samba or the Terminal & SSH add-on.
3. In Home Assistant, open Settings > Apps > App Store and reload the store.
4. Install **Sure Finance (All-in-One)** from Local apps, start it, and select
   Open Web UI. The initial container build needs network access.
5. Create the account; then change `onboarding_state` to `closed` and restart.

See `sure_all_in_one/DOCS.md` for security notes and backups.

## Repository install

Add `https://github.com/CookieSource/haos-sure` in Home Assistant under
Settings > Apps > App Store > Repositories. Home Assistant will build the image
when you install this single app.

## Status

The container image has been built and smoke-tested on amd64 with the current
Sure `stable` image: PostgreSQL initialization, Rails migrations, the web UI,
Sidekiq/Redis, and a PostgreSQL backup all passed. It has not yet been tested
inside Home Assistant OS itself. Use test data before storing real personal
financial or banking data.

## License and artwork

This repository is licensed under the GNU AGPL v3. The Sure icon and logo are
from the upstream [Sure repository](https://github.com/we-promise/sure), which
is also distributed under the GNU AGPL v3. This community package is not an
official Sure or Home Assistant release.
