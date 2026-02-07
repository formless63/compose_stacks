# ReadMeABook

Fully Featured audiobook request and downloading engine to bring audiobooks up to speed with the modern automation standards.

**Links:**
* [kikootwo/readmeabook](https://github.com/kikootwo/readmeabook)
* [Container Registry](https://github.com/kikootwo/readmeabook/pkgs/container/readmeabook)


## Quick Start

1. **Get the Repository**
Clone the repository and navigate to the service directory:
```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/readmeabook

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

* Update `PUBLIC_URL` and `_DIR` paths to match your system.
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
| `APP_PORT` | Port for the web interface | `3030` | Change if port is already in use |
| `PUID` / `PGID` | User and Group ID for file permissions | `1000` | Set to your host user ID (run `id $USER`) |
| `PUBLIC_URL` | The URL used to access the site | `http://localhost:3030` | Set to your actual domain (e.g., `https://audio.example.com`). **Must be a full URL**, not a filepath. |
| `MEDIA_DIR` | Directory containing your audiobooks | `./media` | Use absolute path (e.g., `/mnt/media/audiobooks`) |
| `DOWNLOADS_DIR` | Directory for download client | `./downloads` | Map to your existing downloads folder |
| `CONFIG_DIR` | Application configuration data | `./config` | Use persistent path (e.g., `/mnt/storage/readmeabook/config`) |
| `DB_DIR` | Database storage | `./pgdata` | Use persistent path (e.g., `/mnt/storage/readmeabook/db`) |
| `REDIS_DIR` | Redis storage | `./redis` | Use persistent path (e.g., `/mnt/storage/readmeabook/redis`) |
