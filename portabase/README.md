# Portabase

A database backup dashboard with PostgreSQL.

**Links:**
* [Upstream project](https://github.com/Portabase/portabase)
* [Container registry](https://hub.docker.com/r/portabase/portabase)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/portabase
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

* Set `PROJECT_URL`, `POSTGRES_PASSWORD` and your `_DIR` paths.
* Generate `PROJECT_SECRET` with `openssl rand -hex 32`.
* Set the timezone and image versions in `.env`.
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
| `HOST_PORT` | Web interface port | `8887` | Set in `.env` for your host |
| `PROJECT_URL` | Public URL | `Your dashboard URL` | Set in `.env` for your host |
| `PROJECT_SECRET` | Application secret | `Generate a unique value` | Set in `.env` for your host |
| `PORTABASE_IMAGE / POSTGRES_IMAGE` | Application / database versions | `See .env.example` | Set in `.env` for your host |
| `POSTGRES_PASSWORD` | Database password | `Set a strong password` | Set in `.env` for your host |
| `DATA_DIR / DB_DIR` | Application / database storage | `./data / ./db` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/portabase.md)
