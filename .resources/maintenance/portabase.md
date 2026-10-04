# Portabase

A database backup dashboard with its own PostgreSQL database.

[Upstream documentation](https://portabase.io/docs/dashboard/setup) · [Validation results](../validation/README.md)

## Start

Clone this repository, then run commands from `portabase/`.

```sh
cp .env.example .env
# Edit .env; generate required secrets and configure URLs/storage.
docker compose config --quiet
docker compose up -d
docker compose logs --tail=100
```

## Configuration and compatibility

Set `PROJECT_NAME`, `PROJECT_URL`, `PROJECT_SECRET` (`openssl rand -hex 32`), and PostgreSQL credentials. `POSTGRES_HOST=portabase-pg` points to the bundled database. URL-encode reserved characters in the database password. `PROJECT_URL` also supplies the trusted application origin.

`HOST_PORT=8887` is ready for a normal Docker host. To restrict exposure, use `127.0.0.1:8887` or a real host interface address. Complete the upstream onboarding screen after first launch.

The normal stack needs no pre-existing proxy network. If your reverse proxy uses an external network, set `PROXY_NETWORK` (default `newt_net`) and deploy with:

```sh
docker compose -f compose.yml -f compose.proxy.yml up -d
```

Create that network separately if it does not exist. The overlay connects only the dashboard; PostgreSQL remains on the stack network. `PORTABASE_IMAGE` can select a version or digest.

Back up both `DATA_DIR` (default `./data`) and `DB_DIR` (default `./db`). PostgreSQL remains on major version 17; its data path is unchanged. The dashboard's `/api/health` check follows upstream. Read release notes before upgrades and verify agents can still connect afterwards.

## Maintenance

Back up persistent data before an upgrade. Choose a tested image tag or digest, consult upstream migration notes, then pull and recreate the stack. Keep the previous image reference and a restorable backup; database migrations can make a simple image rollback unsafe.

Container/network names, image selections and deployment paths are configurable in `.env`. Defaults preserve the original container and network names where present. Existing bind-mount paths are retained.
