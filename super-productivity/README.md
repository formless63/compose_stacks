# Super Productivity

The Super Productivity web app with a SuperSync server and PostgreSQL.

**Links:**
* [Upstream project](https://github.com/super-productivity/super-productivity)
* [Container registry](https://github.com/formless63/docker-builds/pkgs/container/supersync)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/super-productivity
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

* Set the app and sync HTTPS URLs, `HOSTNAME` and SMTP settings.
* Generate `JWT_SECRET` with `openssl rand -hex 32` and set `POSTGRES_PASSWORD`.
* Set your `_DIR` paths. The sync data folder must be writable by UID/GID 1001. With default paths: `mkdir -p ./supersync/data && sudo chown 1001:1001 ./supersync/data`.
* Your community image remains the default; switching to the upstream image is optional.
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
| `SYNC_PORT / WEB_PORT` | Sync server / web app ports | `1900 / 8080` | Set in `.env` for your host |
| `APP_PUBLIC_URL / SYNC_PUBLIC_URL` | Public HTTPS URLs | `Your app and sync domains` | Set in `.env` for your host |
| `JWT_SECRET` | Session secret | `Generate a unique value` | Set in `.env` for your host |
| `POSTGRES_PASSWORD` | Database password | `Set a strong password` | Set in `.env` for your host |
| `SUPERSYNC_IMAGE / APP_IMAGE / POSTGRES_IMAGE` | Container images/tags | `See .env.example` | Set in `.env` for your host |
| `DB_DATA_DIR / SUPERSYNC_DATA_DIR` | Database / application storage | `./supersync/db / ./supersync/data` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/super-productivity.md)
