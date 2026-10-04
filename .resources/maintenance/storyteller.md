# Storyteller

A self-hosted platform for ebooks and audiobooks with synchronized narration.

[Upstream documentation](https://storyteller-platform.dev/docs/installation/self-hosting/) · [Validation results](../validation/README.md)

## Start

Clone this repository, then run commands from `storyteller/`.

```sh
cp .env.example .env
# Edit .env; generate required secrets and configure URLs/storage.
docker compose config --quiet
docker compose up -d
docker compose logs --tail=100
```

## Configuration and compatibility

Generate `STORYTELLER_SECRET_KEY` with `openssl rand -base64 32`. Set `AUTH_URL` to the public authentication endpoint, including `/api/v2/auth`, for example `https://books.example.com/api/v2/auth`. The Compose file now uses the same variable as the environment example.

The app is published on `APP_PORT` (8001 by default). `ENABLE_WEB_READER` is configurable. `STORYTELLER_IMAGE` can select a release or immutable digest; the default retains the existing upstream image.

`DATA_DIR` keeps the existing `/data` mapping. Keep its database, books and generated files together in backups, and retain the secret. Ensure the image's runtime user can write this directory. Do not add a guessed UID override: check the image version's upstream instructions.

Read upstream release notes before updating. OAuth configuration and narration/import behavior require a real provider and representative media; a basic startup check does not cover those integrations.

## Maintenance

Back up persistent data before an upgrade. Choose a tested image tag or digest, consult upstream migration notes, then pull and recreate the stack. Keep the previous image reference and a restorable backup; database migrations can make a simple image rollback unsafe.

Container/network names, image selections and deployment paths are configurable in `.env`. Defaults preserve the original container and network names where present. Existing bind-mount paths are retained.
