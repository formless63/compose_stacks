# Penpot

A self-hosted design workspace with frontend, backend, exporter, admin console, MCP, PostgreSQL and Valkey.

[Upstream documentation](https://help.penpot.app/technical-guide/getting-started/docker/) · [Validation results](../validation/README.md)

## Start

Clone this repository, then run commands from `penpot/`. Complete the configuration and storage preparation below before launching.

```sh
cp .env.example .env
# Edit .env; generate required secrets and configure URLs/storage.
docker compose config --quiet
docker compose up -d
docker compose logs --tail=100
```

## Configuration and compatibility

The three original application services plus admin-console and MCP follow upstream 2.18.1. All Penpot images share `PENPOT_VERSION`; upgrade them together. PostgreSQL stays on major version 15 and Valkey on 8.1.

Set `PENPOT_PUBLIC_URI` to your public HTTPS URL. Generate `PENPOT_SECRET_KEY`:

```sh
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Set `POSTGRES_PASSWORD` for a new deployment. The backend uses it automatically; `PENPOT_DATABASE_PASSWORD` remains an optional override for existing configurations. For an existing database, use its current password: changing the Postgres environment variable does not change a database user's password.

Configure `PENPOT_SMTP_*` for your provider. Use TLS on port 587 or SSL on port 465 as appropriate. Flags enable SMTP, administrative access, telemetry, the admin console and MCP. Secure session cookies remain enabled, so use HTTPS. The exporter uses the public URL for users and `PENPOT_INTERNAL_URI` for container-to-container access.

The frontend is published on `PENPOT_HTTP_PORT` (9001 by default). Backend, exporter, admin console, MCP and databases remain on the project network. The proxy needs WebSockets and request body limits at least as large as the configured limits.

The tested Penpot image runs as UID/GID 1001. Prepare the shared assets bind directory before first launch. For the default path:

```sh
mkdir -p ./penpot/assets
sudo chown 1001:1001 ./penpot/assets
```

Use your configured `ASSETS_VOLUME` if overridden; keep it writable by UID/GID 1001. All application services share this directory. The PostgreSQL container manages the database directory separately.

Back up both `DB_VOLUME` and `ASSETS_VOLUME`. Read release migration notes before changing the pinned release. A PostgreSQL major upgrade needs a dump/restore or supported `pg_upgrade`, never just a replacement image tag.

## Maintenance

Back up persistent data before an upgrade. Choose a tested image tag or digest, consult upstream migration notes, then pull and recreate the stack. Keep the previous image reference and a restorable backup; database migrations can make a simple image rollback unsafe.

Container/network names, image selections and deployment paths are configurable in `.env`. Defaults preserve the original container and network names where present. Existing bind-mount paths are retained.
