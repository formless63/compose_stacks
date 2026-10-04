# BitMappery

A browser-based image editor.

**Links:**
* [Upstream project](https://github.com/igorski/bitmappery)
* [Container registry](https://github.com/formless63/docker-builds/pkgs/container/bitmappery)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/bitmappery
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

* Change `APP_PORT` if port 5173 is already in use.
* Choose `BITMAPPERY_IMAGE` in `.env`; use a dated tag or digest to keep the same version across updates.
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
| `APP_PORT` | Web interface port | `5173` | Set in `.env` for your host |
| `BITMAPPERY_IMAGE` | Container image/tag | `ghcr.io/formless63/bitmappery:latest` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/bitmappery.md)
