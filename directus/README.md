# Directus

Directus with Redis, connecting to your existing PostgreSQL database.

**Links:**
* [Upstream project](https://github.com/directus/directus)
* [Container registry](https://hub.docker.com/r/directus/directus)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/directus
```

2. **Prepare Environment**
   Copy the example configuration file:
```bash
cp external-db-.env.example .env
```

3. **Edit Configuration**
   Open the configuration file:
```bash
nano .env
```

* Set your URL, administrator credentials and `DB_*` connection settings.
* Generate `DIRECTUS_SECRET` with `openssl rand -hex 32`.
* Set your storage paths. Uploads and extensions must be writable by UID 1000. With default paths: `mkdir -p ./uploads ./extensions && sudo chown 1000:1000 ./uploads ./extensions`.
* **Save & Exit:** Press `Ctrl+X`, then `Y`, then `Enter`.

4. **Launch**
   Start the stack:
```bash
docker compose --env-file .env -f external-db-compose.yaml up -d
```

5. **Verify**
   Check the startup logs:
```bash
docker compose --env-file .env -f external-db-compose.yaml logs -f
```

*(Press `Ctrl+C` to exit logs.)*

## Configuration

Edit deployment settings in `.env`; keep it when pulling repository updates. Image selections, ports, paths and supported application settings are listed in the environment example. `latest` is a rolling tag; choose a release tag or digest if you want a fixed version.

| Variable | Description | Default | Recommendation |
| --- | --- | --- | --- |
| `DIRECTUS_PORT` | Web interface port | `8055` | Set in `.env` for your host |
| `DIRECTUS_PUBLIC_URL` | Public URL | `Your Directus domain` | Set in `.env` for your host |
| `DIRECTUS_VERSION / REDIS_VERSION` | Application / cache versions | `See .env.example` | Set in `.env` for your host |
| `DIRECTUS_SECRET` | Application secret | `Generate a unique value` | Set in `.env` for your host |
| `DIRECTUS_ADMIN_EMAIL / DIRECTUS_ADMIN_PASSWORD` | Initial administrator | `Choose your credentials` | Set in `.env` for your host |
| `DB_*` | Existing database connection | `Your database settings` | Set in `.env` for your host |
| `DIRECTUS_UPLOADS_DIR / DIRECTUS_EXTENSIONS_DIR` | Persistent application files | `./uploads / ./extensions` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/directus.md)
