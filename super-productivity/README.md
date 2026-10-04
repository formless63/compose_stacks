# Super Productivity and SuperSync

The Super Productivity web app, a SuperSync server, and PostgreSQL.

[Upstream documentation](https://github.com/super-productivity/super-productivity/tree/master/packages/super-sync-server) · [Validation results](../VALIDATION.md)

## Start

Clone this repository, then run commands from `super-productivity/`. Complete the configuration and storage preparation below before launching.

```sh
cp .env.example .env
# Edit .env; generate required secrets and configure URLs/storage.
docker compose config --quiet
docker compose up -d
docker compose logs --tail=100
```

## Configuration and compatibility

Set `APP_PUBLIC_URL` and `SYNC_PUBLIC_URL` to your public HTTPS URLs. Generate `JWT_SECRET` with `openssl rand -hex 32` and set a strong `POSTGRES_PASSWORD`. `HOSTNAME` is the WebAuthn relying-party domain without scheme/port: the sync hostname or a valid parent domain. Keep existing values if users already have passkeys.

Configure SMTP for account verification and recovery. The stack defaults to production, binds the sync server to `0.0.0.0` inside its container, and uses a bounded Prisma database connection pool. URL-encode reserved characters in the database password because it is interpolated into a connection URI.

The `migrate` service runs upstream `scripts/migrate-deploy.sh`; the server starts only after it succeeds. PostgreSQL remains on major version 15 and existing `DB_DATA_DIR` / `SUPERSYNC_DATA_DIR` paths are preserved.

The SuperSync image runs as UID/GID 1001. Before first launch, create its dedicated bind directory and make it writable by that user. For the default path:

```sh
mkdir -p ./supersync/data
sudo chown 1001:1001 ./supersync/data
```

Use your configured `SUPERSYNC_DATA_DIR` instead if overridden. Retain ownership of existing data; the PostgreSQL image manages its own database directory.

For upgrades, back up the database and application data first, then stop the server while migrating:

```sh
docker compose pull
docker compose stop supersync
docker compose run --rm migrate
docker compose up -d
```

A failed migration blocks startup. Read the migrator output and upstream recovery instructions; do not delete database files or mark migrations successful blindly.

`SUPERSYNC_IMAGE` defaults to `ghcr.io/formless63/supersync:latest`. This image remains supported. To opt into the creator's image, set it to `ghcr.io/super-productivity/supersync:latest`; both the migration job and server use that setting. First pin and back up your working deployment, compare upstream versions, and test the switch against a restored copy. Switching images does not move, reset, or downgrade your database. The community startup notice can be hidden with `SUPERSYNC_HIDE_UPSTREAM_NOTICE=true` in the container environment.

Check `http://localhost:1900/health` for a healthy database connection. Proxy the app to port 8080 and sync API/WebSockets to port 1900. Preserve HTTPS and WebSocket support.

## Maintenance

Back up persistent data before an upgrade. Choose a tested image tag or digest, consult upstream migration notes, then pull and recreate the stack. Keep the previous image reference and a restorable backup; database migrations can make a simple image rollback unsafe.

Fixed container names have been removed so separate Compose projects can coexist. Scripts using old container names should use `docker compose exec SERVICE` instead. Existing bind-mount paths are retained.
