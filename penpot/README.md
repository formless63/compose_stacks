# Penpot

Open-source collaborative design tool (Figma-like) you can fully self-host.
This stack runs the official **frontend**, **backend**, **exporter**, **Postgres**, and **Valkey (Redis-compatible)** services.
This example was built with the following desires:
* SMTP required
* bind mounts only (no named volumes)
* env-driven configuration
* `:latest` allowed but version pinning recommended
* no Traefik, no mailcatch, HTTPS behind a reverse proxy like [Pangolin](https://docs.pangolin.net/)

**Links:**

* GitHub: [https://github.com/penpot/penpot](https://github.com/penpot/penpot)
* Docker Hub: [https://hub.docker.com/u/penpotapp](https://hub.docker.com/u/penpotapp)
* Docs: [https://help.penpot.app/technical-guide/getting-started/docker/](https://help.penpot.app/technical-guide/getting-started/docker/)

---

## Quick Start

### 1. Get the Repository

Clone and navigate to this stack:

```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/penpot
```

---

### 2. Prepare Environment

Copy the example configuration:

```bash
cp .env.example .env
```

---

### 3. Edit Configuration

```bash
nano .env
```

Update at minimum:

* `PENPOT_PUBLIC_URI` → your real HTTPS URL (required)
* `PENPOT_SECRET_KEY` → generate a strong key
* SMTP settings
* `DB_VOLUME` / `ASSETS_VOLUME` paths

Generate a key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Save & exit.

---

### 4. Launch

```bash
docker compose up -d
```

---

### 5. Verify

```bash
docker compose logs -f
```

Then open:

```
https://sub.domain.com
```

---

## Reverse Proxy 

Route your domain to:

```
penpot-frontend:8080  #if you've made available via docker networks
IP-Address:Port  #if you're not using docker networking
```

Requirements:

* HTTPS
* WebSockets enabled
* Upload/body size ≥ 350MB (matches Penpot limits)

---

## Services Overview

| Service  | Purpose                              |
| -------- | ------------------------------------ |
| frontend | Web UI + public entrypoint           |
| backend  | Core API, auth, persistence          |
| exporter | Handles PNG/PDF/SVG exports          |
| postgres | Database                             |
| valkey   | Redis-compatible cache/notifications |

All persistent data is stored via bind mounts.

---

## Configuration

| Variable            | Description            | Default             | Recommendation              |
| ------------------- | ---------------------- | ------------------- | --------------------------- |
| `PENPOT_PUBLIC_URI` | Public HTTPS URL       | —                   | **Required**                |
| `PENPOT_VERSION`    | Image tag              | `latest`            | Pin in production           |
| `PENPOT_SECRET_KEY` | Session/encryption key | change-me           | Generate strong random      |
| `PENPOT_FLAGS`      | Feature toggles        | see example         | Leave default unless needed |
| `PENPOT_HTTP_PORT`  | Local bind port        | `9001`              | Any free port               |
| `DB_VOLUME`         | Postgres data dir      | `./penpot/postgres` | Persistent disk             |
| `ASSETS_VOLUME`     | User files/assets      | `./penpot/assets`   | Persistent disk             |
| `PENPOT_DATABASE_*` | DB credentials         | penpot/penpot       | Change if desired           |
| `PENPOT_REDIS_URI`  | Redis/Valkey URI       | internal            | Leave default               |
| `PENPOT_SMTP_*`     | SMTP settings          | —                   | **Required for invites**    |

---

## Storage Layout

```
./penpot/
  ├─ postgres/   # database files
  └─ assets/     # uploaded files, exports, images
```

Back up **both** directories.

---

## Updating

```bash
docker compose pull
docker compose up -d
```

If using `latest`, updates are automatic on pull.
For stability, pin a specific version:

```
PENPOT_VERSION=2.4.0
```

---

## Notes

* Do **not** change `/opt/data/assets` inside the container.
  Change `ASSETS_VOLUME` instead.
* SMTP is strongly recommended for team invites.
* Removing the exporter disables file exports.
* Postgres + assets must both be backed up.
