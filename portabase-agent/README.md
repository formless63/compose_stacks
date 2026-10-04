# Portabase agent

Connects your Portabase dashboard to database services for backups.

**Links:**
* [Upstream project](https://github.com/Portabase/agent)
* [Container registry](https://hub.docker.com/r/portabase/agent)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/portabase-agent
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

* Paste your dashboard-issued `EDGE_KEY`.
* Set the database network names and `AGENT_DIR`. Both networks must already exist; for one shared network, use its name for both.
* Create a valid configuration file: `cp databases.example.json databases.json`. Fill it using the dashboard/upstream instructions.
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
| `EDGE_KEY` | Agent key from the dashboard | `Paste your dashboard key` | Set in `.env` for your host |
| `AGENT_IMAGE` | Container image/tag | `portabase/agent:latest` | Set in `.env` for your host |
| `AGENT_DIR` | Folder containing databases.json | `Current directory` | Set in `.env` for your host |
| `DATABASE_NETWORK_1 / DATABASE_NETWORK_2` | Existing database networks | `Choose your Docker networks` | Set in `.env` for your host |
| `POLLING` | Polling interval in seconds | `5` | Set in `.env` for your host |
| `TZ` | Timezone | `UTC` | Set in `.env` for your host |

[Update and advanced setup notes](../.resources/maintenance/portabase-agent.md)
