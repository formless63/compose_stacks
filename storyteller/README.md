# Storyteller

A self-hosted platform for syncing and playing audiobooks with guided narration (epubs/audio).

**Links:**
* [Official Documentation](https://storyteller-platform.gitlab.io/storyteller/docs/installation/self-hosting)
* [GitLab Repository](https://gitlab.com/storyteller-platform/storyteller)

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


3. **Generate Secret Key (Required)**
Storyteller will not start without a secure unique key. Run this command and paste the output into your `.env` file:
```bash
openssl rand -base64 32

```


4. **Edit Configuration**
Open the configuration file:
```bash
nano .env

```


* Paste your generated `STORYTELLER_SECRET_KEY`.
* Update `DATA_DIR` to your book library location.
* **Save & Exit:** `Ctrl+X`, `Y`, `Enter`.


5. **Launch**
Start the stack:
```bash
docker compose up -d

```



## Configuration

| Variable | Description | Default | Recommendation |
| --- | --- | --- | --- |
| `APP_PORT` | Web Interface Port | `8001` | Change if in use |
| `STORYTELLER_SECRET_KEY` | **Required** Encryption Key | `N/A` | Must be generated manually |
| `ENABLE_WEB_READER` | Web-based playback | `false` | Set to `true` to try the beta player |
| `PUBLIC_URL` | External URL | `http://localhost:8001` | Required if using OAuth features |
| `DATA_DIR` | Library Storage | `./data` | Map to your media folder (e.g. `/mnt/media/books`) |
