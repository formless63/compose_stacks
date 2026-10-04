# BitMappery

A browser image editor served as a production static site by nginx.

[Upstream documentation](https://github.com/igorski/bitmappery) · [Validation results](../validation/README.md)

## Start

Clone this repository, then run commands from `bitmappery/`.

```sh
cp .env.example .env
# Edit .env; generate required secrets and configure URLs/storage.
docker compose config --quiet
docker compose up -d
docker compose logs --tail=100
```

## Configuration and compatibility

Open `http://localhost:5173` (or your chosen `APP_PORT`). No persistent container storage is required; save your work from the browser. The new production image retains container port 5173. `BITMAPPERY_IMAGE` can select a dated tag or digest from the community build repository.

## Maintenance

Back up persistent data before an upgrade. Choose a tested image tag or digest, consult upstream migration notes, then pull and recreate the stack. Keep the previous image reference and a restorable backup; database migrations can make a simple image rollback unsafe.

Container/network names, image selections and deployment paths are configurable in `.env`. Defaults preserve the original container and network names where present. Existing bind-mount paths are retained.
