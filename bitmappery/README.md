# BitMappery

A self-hosted instance of [BitMappery](https://www.igorski.nl/bitmappery), a free, browser-based pixel art editor. It is a Progressive Web App (PWA) that works offline and saves data locally to your browser. This container is being built from the official repo via github actions within my [docker-builds repo](https://github.com/formless63/docker-builds).

**Links:**
* [GitHub: igorski/bitmappery](https://github.com/igorski/bitmappery)
* [Container Registry: ghcr.io/formless63/bitmappery](https://github.com/formless63/docker-builds/pkgs/container/bitmappery)

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
(Optional) Open the configuration file if you need to change the port:

```bash
nano .env

```

* Update `APP_PORT` if port 8080 is already in use on your system.
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
| `APP_PORT` | Port for the web interface | `5173` | Change if port is in use |

## Data Persistence

BitMappery is a **client-side application**.

* **Projects:** Saved in your browser's Local Storage (IndexedDB).
* **Exports:** Saved as `.rle` or image files to your computer.
* **Server Data:** This container is stateless. No server-side volumes are required.
