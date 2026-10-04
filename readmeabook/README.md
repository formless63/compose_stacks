# ReadMeABook

An audiobook request and library application.

**Links:**
* [Upstream project](https://github.com/kikootwo/readmeabook)
* [Container registry](https://github.com/kikootwo/readmeabook/pkgs/container/readmeabook)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/readmeabook
```

2. **Prepare Environment**
   Copy the example configuration file:
```bash
cp .env.example .env
```

3. **Edit Configuration**
   Open the configuration file:
```bash
nano .env
```

* Set `PUBLIC_URL`, your `_DIR` paths and `PUID`/`PGID` (run `id` on your host).
* Keep download paths consistent with your download client.
* Choose the image version in `.env`.
* **Save & Exit:** Press `Ctrl+X`, then `Y`, then `Enter`.

4. **Launch**
   Start the stack:
```bash
docker compose up -d
```

5. **Verify**
   Check the startup logs:
```bash
docker compose logs -f
```

*(Press `Ctrl+C` to exit logs.)*

## Configuration

Edit deployment settings in `.env`; keep it when pulling repository updates. Image selections, ports, paths and supported application settings are listed in the environment example. `latest` is a rolling tag; choose a release tag or digest if you want a fixed version.

| Variable | Description | Default | Recommendation |
| --- | --- | --- | --- |
| `APP_PORT` | Web interface port | `3030` | Set in `.env` for your host |
| `PUBLIC_URL` | URL users open | `http://localhost:3030` | Set in `.env` for your host |
| `READMEABOOK_IMAGE` | Container image/tag | `ghcr.io/kikootwo/readmeabook:latest` | Set in `.env` for your host |
| `PUID / PGID` | Application file ownership | `1000 / 1000` | Set in `.env` for your host |
| `CONFIG_DIR / CACHE_DIR` | Application settings / cache | `./config / ./cache` | Set in `.env` for your host |
| `DOWNLOADS_DIR / MEDIA_DIR` | Downloads / library | `./downloads / ./media` | Set in `.env` for your host |
| `DB_DIR / REDIS_DIR` | Database / cache storage | `./pgdata / ./redis` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/readmeabook.md)
