# portabase-agent

The lightweight, remote execution agent for Portabase. Deploy this agent on any Docker host to securely communicate with your central Portabase dashboard and execute automated database backups.

## Quick Start

1. **Get the Repository**
Clone the repository and navigate to the agent directory:
```bash
   git clone https://github.com/formless63/compose_stacks.git
   cd compose_stacks/portabase-agent

```

2. **Prepare Environment**
Copy the example configuration file:
```bash
cp .env.example .env

```


3. **Initialize Configuration File**
Create the empty JSON configuration file. **Do not skip this step**, or Docker will create a directory instead of a file, causing the container to crash:
```bash
touch databases.json

```


4. **Edit Configuration**
Open the configuration file:
```bash
nano .env

```


* Paste the `EDGE_KEY` generated from your Portabase dashboard.
* Define your `AGENT_DIR` if you aren't storing `databases.json` in the current working directory.


5. **Network Preparation**
The compose file defines `service1_net` and `service2_net` as external. Ensure these networks exist (they should be the networks where your target databases reside):
```bash
docker network ls
# If missing, create them or update the compose file to match your existing database networks

```


6. **Launch**
Start the stack in detached mode:
```bash
docker compose up -d

```


7. **Verify**
Check the logs to ensure the agent authenticated with the dashboard successfully:
```bash
docker compose logs -f

```



## Configuration

### Environment Variables (.env)

| Variable | Description | Default | Recommendation |
| --- | --- | --- | --- |
| `AGENT_DIR` | Host path containing `databases.json` | `.` (Current Dir) | Leave blank for current directory, or specify an absolute path |
| `TZ` | Timezone for cron schedules and logs | `UTC` | Match your host or Portabase dashboard timezone |
| `EDGE_KEY` | Authentication key from Portabase dashboard | *(Empty)* | **Required.** Paste the exact key from the dashboard UI |

### Agent Service Settings (docker-compose.yml)

| Variable | Description | Default | Notes |
| --- | --- | --- | --- |
| `POLLING` | Frequency (in seconds) the agent checks for jobs | `5` | Decrease to `10` or `15` if you have many agents to reduce dashboard load |
| `APP_ENV` | Application execution context | `production` | Leave as default |
| `LOG` | Logging verbosity | `info` | Change to `debug` for troubleshooting connection issues |
| `extra_hosts` | Host resolution overrides | `localhost:host-gateway` | Allows the agent to backup databases mapped directly to the host's loopback interface |
