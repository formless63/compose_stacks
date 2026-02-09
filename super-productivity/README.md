# Super Productivity

A self-hosted stack for [Super Productivity](https://super-productivity.com/), using a github-actions-built SuperSync Docker image to enable native syncing across devices. This repo assumes you will use a reverse proxy and serve your instance with a fully qualified domain name.

**Links:**
* [GitHub: super-productivity/super-productivity](https://github.com/super-productivity/super-productivity)
* [Container Registry: ghcr.io/formless63/supersync](https://github.com/formless63/docker-builds/pkgs/container/supersync)

## Quick Start

1. **Get the Repository**
   Clone the repository and navigate to the service directory:
```bash
   git clone https://github.com/formless63/compose_stacks.git
   cd compose_stacks/supersync

```

2. **Prepare Environment**
Copy the example configuration file:

```bash
cp .env.example .env

```

3. **Edit Configuration**
Open the configuration file with nano:

```bash
nano .env

```

* Update `APP_PUBLIC_URL` and `SYNC_PUBLIC_URL` to match your domain/subdomains.
* Update `POSTGRES_PASSWORD` with a unique password for your database.
* **Generate a Secret:** Run `openssl rand -hex 32` and paste the result into `JWT_SECRET`.
* Set `DB_DATA_DIR` and `SUPERSYNC_DATA_DIR` to your preferred bind locations (eg. /mnt/super-productivity/...)
* **Save & Exit:** Press `Ctrl+X`, then `Y`, then `Enter`.

4. **Launch**
Start the stack in detached mode:

```bash
docker compose up -d

```

5. **Verify**
Check the logs to ensure everything started correctly:

```bash
docker compose logs -f

```

*(Press `Ctrl+C` to exit logs)*

## Configuration

| Variable | Description | Default | Recommendation |
| --- | --- | --- | --- |
| `SYNC_PORT` | Port for the SuperSync Server | `1900` | Change if port is in use |
| `WEB_PORT` | Port for the Super Productivity App | `8080` | Change if port is in use |
| `APP_PUBLIC_URL` | The URL of your Frontend App | `https://sp.domain.com` | Must match your browser URL for CORS to work |
| `SYNC_PUBLIC_URL` | The URL of your Sync Server | `https://sp-sync.domain.com` | Used as your sync target |
| `JWT_SECRET` | Encryption secret for sessions | `change_me` | **REQUIRED:** Generate a random 32-char string |
| `POSTGRES_PASSWORD` | Database password | `change_this_password` | Set a strong password |
| `DB_DATA_DIR` | Database storage path | `./supersync/db` | Keep on persistent storage |
| `SUPERSYNC_DATA_DIR` | File upload storage path | `./supersync/data` | Keep on persistent storage |
| `NODE_ENV` | Application Mode | `development` | Switch to `production` when stable |

## SMTP Configuration (Optional)
To enable: uncomment the SMTP section in `compose.yaml` and set these variables in `.env`.

| Variable | Description | Default | Recommendation |
| --- | --- | --- | --- |
| `SMTP_HOST` | Mail server hostname | `[None]` | e.g., `smtp.gmail.com` |
| `SMTP_PORT` | Mail server port | `587` | Use `465` for SSL or `587` for TLS |
| `SMTP_SECURE` | Use SSL/TLS connection | `false` | Set to `true` if using port 465 |
| `SMTP_USER` | SMTP Username | `[None]` | Usually your email address |
| `SMTP_PASS` | SMTP Password | `[None]` | Use an App Password where appropriate |
| `SMTP_FROM` | The "From" address in emails | `[None]` | e.g., `noreply@yourdomain.com` |
