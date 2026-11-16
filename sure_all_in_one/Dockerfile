# Single-container HAOS package: uses Sure's upstream production image.
# Built for amd64 only. Build source is local to the Home Assistant Supervisor.
FROM ghcr.io/we-promise/sure:stable
USER root

# Install PostgreSQL 16 from PostgreSQL's Debian repository, plus Redis and a
# small process supervisor. None of the database/cache ports are published.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl gnupg; \
    install -d -m 0755 /usr/share/keyrings; \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --batch --yes --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg; \
    . /etc/os-release; \
    echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] https://apt.postgresql.org/pub/repos/apt ${VERSION_CODENAME}-pgdg main" > /etc/apt/sources.list.d/pgdg.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends postgresql-16 redis-server supervisor nginx gosu jq openssl; \
    pg_dropcluster --stop 16 main || true; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*; \
    rm -rf /rails/storage; \
    ln -s /data/storage /rails/storage

COPY scripts/ /usr/local/bin/
COPY supervisor/sure.conf /etc/supervisor/conf.d/sure.conf
COPY ingress/nginx.conf /etc/nginx/nginx.conf
COPY ingress/direct-http.conf ingress/direct-tls.conf /etc/nginx/
RUN chmod 0755 /usr/local/bin/sure-ha-init /usr/local/bin/sure-db-init \
    /usr/local/bin/sure-web /usr/local/bin/sure-worker \
    /usr/local/bin/sure-backup-loop /usr/local/bin/sure-backup-now

ENV RAILS_ENV=production \
    RACK_ENV=production \
    SELF_HOSTED=true \
    DB_HOST=127.0.0.1 \
    DB_PORT=5432 \
    POSTGRES_USER=sure_user \
    POSTGRES_DB=sure_production \
    REDIS_URL=redis://127.0.0.1:6379/1 \
    BINDING=0.0.0.0 \
    PORT=3000 \
    WEB_CONCURRENCY=1 \
    RAILS_MAX_THREADS=3 \
    RAILS_FORCE_SSL=false \
    POSTHOG_FEEDBACK_ENABLED=false \
    TZ=Europe/Amsterdam

WORKDIR /rails
EXPOSE 3000 3443 8099
STOPSIGNAL SIGTERM
ENTRYPOINT ["/usr/local/bin/sure-ha-init"]
CMD []
