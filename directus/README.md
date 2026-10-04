# Directus with external PostgreSQL

Directus and a private Redis cache, connecting to an existing PostgreSQL database.

[Upstream documentation](https://directus.io/docs/self-hosting/overview) · [Validation results](../VALIDATION.md)

## Start

Clone this repository, then run commands from `directus/`. Complete the configuration and storage preparation below before launching.

Use the explicit Compose and environment filenames shown below.

## Configuration and compatibility

This folder uses nonstandard filenames:

```sh
cp external-db-.env.example .env
# Edit .env before running these commands.
docker compose --env-file .env -f external-db-compose.yaml config --quiet
docker compose --env-file .env -f external-db-compose.yaml up -d
```

Set `DIRECTUS_SECRET` (`openssl rand -hex 32`), initial administrator credentials, `DIRECTUS_PUBLIC_URL`, and the `DB_*` connection settings. The database must exist and the user must have migration permissions. Administrator credentials bootstrap a new database; changing them later does not reset an existing account.

`DB_HOST` must be reachable from inside the container. For a database on another Docker network, attach the Directus service to that external network and use the database service's DNS name. For an external machine, use its reachable DNS name/IP; container `localhost` refers to Directus itself. Redis stays private, and Directus waits until it is healthy.

Port `DIRECTUS_PORT` (8055 by default) exposes the app. The health check probes the public `/server/ping` endpoint with Node's built-in HTTP client. `DIRECTUS_VERSION` selects the application release; Redis defaults to `8-alpine`. Pin a tested application version or digest for production.

Keep uploads and extensions writable by the image's `node` user (typically UID 1000).
For the default paths on a new deployment:

```sh
mkdir -p ./uploads ./extensions
sudo chown 1000:1000 ./uploads ./extensions
```

Use the paths configured in `.env` if overridden. Back up the external database, uploads and extension files together before updating. Redis is a cache, not the authoritative database.

## Maintenance

Back up persistent data before an upgrade. Choose a tested image tag or digest, consult upstream migration notes, then pull and recreate the stack. Keep the previous image reference and a restorable backup; database migrations can make a simple image rollback unsafe.

Fixed container names have been removed so separate Compose projects can coexist. Scripts using old container names should use `docker compose exec SERVICE` instead. Existing bind-mount paths are retained.
