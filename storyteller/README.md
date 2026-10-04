# Storyteller

A self-hosted platform for ebooks and audiobooks with synchronized narration.

**Links:**
* [Upstream project](https://gitlab.com/storyteller-platform/storyteller)
* [Container registry](https://gitlab.com/storyteller-platform/storyteller/container_registry)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/storyteller
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

* Generate `STORYTELLER_SECRET_KEY` with `openssl rand -base64 32`.
* Set `AUTH_URL`, including `/api/v2/auth`, and your `DATA_DIR`.
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
| `APP_PORT` | Web interface port | `8001` | Set in `.env` for your host |
| `AUTH_URL` | Public authentication URL | `https://books.example.com/api/v2/auth` | Set in `.env` for your host |
| `STORYTELLER_IMAGE` | Container image/tag | `See .env.example` | Set in `.env` for your host |
| `STORYTELLER_SECRET_KEY` | Application secret | `Generate a unique value` | Set in `.env` for your host |
| `DATA_DIR` | Persistent books and database | `./data` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/storyteller.md)
