# portabase

Portabase is the 100% open source and self-hosted solution to centralize, secure, and automate your database backups.

**Links:**
* [Portabase/portabase](https://github.com/Portabase/portabase)
* [Docker Hub / Container Registry](https://hub.docker.com/r/portabase/portabase)

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


3. **Pre-requisites**
Ensure external Docker networks exists before starting the stack - this example uses newt_net assuming a Pangolin environment. Comment out the newt_net blocks if not using.


4. **Edit Configuration**
Open the configuration file:
```bash
nano .env
```


* Generate a strong `PROJECT_SECRET` (e.g., run `openssl rand -hex 32` in your terminal).
* Update `HOST_PORT` with a valid port or IP/Port binding.
* Provide a secure `POSTGRES_PASSWORD`.


5. **Launch**
Start the stack in detached mode:
```bash
docker compose up -d
```


6. **Verify**
Check the logs to ensure everything started correctly and the database is healthy:
```bash
docker compose logs -f
```

*(Press `Ctrl+C` to exit logs)*

## Configuration

| Variable | Description | Default / Example | Recommendation |
| --- | --- | --- | --- |
| `HOST_PORT` | Host interface and port binding | `8887` | Bind to a port or specific interface (e.g., Tailscale IP) or `0.0.0.0:8887` |
| `PROJECT_NAME` | Internal name for the deployment | `portabase-dashboard` | Leave as default unless managing multiple instances |
| `PROJECT_URL` | The external URL used to access Portabase | `https://portabase.domain.com` | Match your reverse proxy or public domain |
| `PROJECT_SECRET` | Encryption key for agent communication | *(Empty)* | **Required.** Generate via `openssl rand -hex 32` |
| `POSTGRES_DB` | Name of the Postgres database | `portabase` | Leave as default |
| `POSTGRES_USER` | Postgres administrative user | `portabase` | Leave as default |
| `POSTGRES_PASSWORD` | Password for the Postgres user | *(Empty)* | **Required.** Generate a strong password |
| `POSTGRES_HOST` | Hostname for the Postgres container | `portabase-pg` | Leave as default (matches compose service name) |
| `DATA_DIR` | Host path for Portabase application data | `./data` | Map to your persistent storage (e.g., `/mnt/data/portabase`) |
| `DB_DIR` | Host path for Postgres database files | `./db` | Map to fast persistent storage (e.g., NVMe/SSD volume) |

