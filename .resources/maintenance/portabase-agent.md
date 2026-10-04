# Portabase agent

An agent that connects the Portabase dashboard to your database services.

[Upstream documentation](https://portabase.io/docs/agent/setup) · [Validation results](../validation/README.md)

## Start

Clone this repository, then run commands from `portabase-agent/`.

```sh
cp .env.example .env
# Edit .env; generate required secrets and configure URLs/storage.
docker compose config --quiet
docker compose up -d
docker compose logs --tail=100
```

## Configuration and compatibility

Set `EDGE_KEY` to the key issued by your dashboard. Prepare the writable JSON configuration file before launching:

```sh
cp databases.example.json databases.json
```

The sample is valid JSON containing an empty `databases` list. Configure actual database entries using the upstream schema/dashboard instructions. `AGENT_DIR` can point to another directory containing this file. The bind mount refuses to create a missing host path, avoiding Docker silently creating a directory.

Set `DATABASE_NETWORK_1` and `DATABASE_NETWORK_2` to existing networks containing the databases. Both must exist; for one shared database network, set both to the same name. Database hostnames are the service/container DNS names on those networks. Change `POLLING` if needed (1–600 seconds; at least 5 is recommended). Compose passes this to the upstream variable `POOLING`, which is its actual spelling; the old container variable `POLLING` was ignored. Larger values reduce polling frequency.

`host.docker.internal` maps to the host gateway. It can reach services listening on that reachable host address; it cannot reach a service bound exclusively to host `127.0.0.1`. `localhost` inside the agent remains the agent itself. Existing database entries that used `localhost` for a host database should use `host.docker.internal` and a reachable host listener.

The configuration mount is writable because the agent may update it. Restrict host access to this file: it can contain database credentials. This example targets network database backups and does not mount the Docker socket. Docker-volume backup features require additional upstream setup and grant broad host access.

Verify registration and a backup/restore of a disposable database against your own dashboard before using this for real backups. An environment key is required for that integration check.

## Maintenance

Back up persistent data before an upgrade. Choose a tested image tag or digest, consult upstream migration notes, then pull and recreate the stack. Keep the previous image reference and a restorable backup; database migrations can make a simple image rollback unsafe.

Container/network names, image selections and deployment paths are configurable in `.env`. Defaults preserve the original container and network names where present. Existing bind-mount paths are retained.
