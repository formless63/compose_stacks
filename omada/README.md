# Omada Controller

A self-hosted TP-Link Omada network controller.

**Links:**
* [Upstream project](https://github.com/mbentley/docker-omada-controller)
* [Container registry](https://hub.docker.com/r/mbentley/omada-controller)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/omada
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

* Set your `_DIR` paths and timezone. Set `PUID`/`PGID` to your host user if needed (run `id`).
* Keep the `6.2` image track unless you intend to upgrade; do not change a v5 installation to v6 without its database migration.
* Devices need to reach the controller discovery/adoption ports. The v6 image also requires a compatible CPU; see the maintenance notes.
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
| `APP_PORT` | HTTPS management port | `8043` | Set in `.env` for your host |
| `OMADA_VERSION` | Image update track | `6.2` | Set in `.env` for your host |
| `OMADA_BIND_IP` | Interface for web/portal ports | `All interfaces` | Set in `.env` for your host |
| `PUID / PGID` | Controller file ownership | `508 / 508` | Set in `.env` for your host |
| `TZ` | Timezone | `Etc/UTC` | Set in `.env` for your host |
| `DATA_DIR / LOGS_DIR` | Controller storage / logs | `./data / ./logs` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/omada.md)
