# ReadMeABook

An audiobook request and library application using the upstream unified container.

[Upstream documentation](https://github.com/kikootwo/readmeabook/blob/main/docker-compose.yml) · [Validation results](../VALIDATION.md)

## Start

Clone this repository, then run commands from `readmeabook/`.

```sh
cp .env.example .env
# Edit .env; generate required secrets and configure URLs/storage.
docker compose config --quiet
docker compose up -d
docker compose logs --tail=100
```

## Configuration and compatibility

The upstream unified container includes PostgreSQL and Redis. All six existing persistence mappings are retained: config, cache, downloads, media, PostgreSQL and Redis. Its `/api/health` endpoint is checked after a 60-second startup allowance.

Set `PUID` / `PGID` to match your host permissions. PostgreSQL retains UID 103 while using the selected group; application/Redis files use your selected UID/GID. LXC setups must account for UID 103. Do not recursively change PostgreSQL data ownership to `PUID`.

Set `PUBLIC_URL` to the URL users actually open, without a trailing slash. It is needed for Plex/OIDC callbacks. If you change `APP_PORT` for local use, update the port in `PUBLIC_URL` too. Complete the first-run setup wizard after launch.

The downloader and this container must see downloaded files at the same container paths. Keep `/downloads` consistent across both services. `READMEABOOK_IMAGE` can select a version or digest.

Back up configuration (including automatically generated secrets), PostgreSQL data and media. Read upstream upgrade notes before pulling a new unified image; bundled database changes may require migration. A startup health check does not verify Plex, OIDC, indexers or download clients.

## Maintenance

Back up persistent data before an upgrade. Choose a tested image tag or digest, consult upstream migration notes, then pull and recreate the stack. Keep the previous image reference and a restorable backup; database migrations can make a simple image rollback unsafe.

Fixed container names have been removed so separate Compose projects can coexist. Scripts using old container names should use `docker compose exec SERVICE` instead. Existing bind-mount paths are retained.
