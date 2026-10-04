# Penpot

A self-hosted design and prototyping workspace.

**Links:**
* [Upstream project](https://github.com/penpot/penpot)
* [Container registry](https://hub.docker.com/u/penpotapp)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/penpot
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

* Set `PENPOT_PUBLIC_URI` and SMTP settings.
* Generate `PENPOT_SECRET_KEY` with `python3 -c "import secrets; print(secrets.token_urlsafe(64))"`.
* Set `POSTGRES_PASSWORD`; the backend uses the same password unless you explicitly override it.
* Set the storage paths. The assets folder must be writable by UID/GID 1001. With default paths: `mkdir -p ./penpot/assets && sudo chown 1001:1001 ./penpot/assets`.
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
| `PENPOT_HTTP_PORT` | Web interface port | `9001` | Set in `.env` for your host |
| `PENPOT_PUBLIC_URI` | Public HTTPS URL | `Your Penpot domain` | Set in `.env` for your host |
| `PENPOT_VERSION / POSTGRES_IMAGE / VALKEY_IMAGE` | Application / database / cache versions | `See .env.example` | Set in `.env` for your host |
| `PENPOT_SECRET_KEY` | Session and invitation secret | `Generate a unique value` | Set in `.env` for your host |
| `POSTGRES_PASSWORD` | Database password | `Set a strong password` | Set in `.env` for your host |
| `DB_VOLUME / ASSETS_VOLUME` | Database / shared files | `./penpot/postgres / ./penpot/assets` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/penpot.md)
