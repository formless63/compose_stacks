# Omada Controller

Docker Compose template for the TP-Link Omada Software Controller using the community-maintained `mbentley/omada-controller` image.

**Links:**
- [mbentley/docker-omada-controller](https://github.com/mbentley/docker-omada-controller)
- [TP-Link Omada Software Controller](https://support.omadanetworks.com/us/product/omada-software-controller/)

## Quick start

```bash
cp .env.example .env
docker compose up -d
```

The controller UI is available on HTTPS port `8043` by default.

## Networking

This template intentionally uses bridge networking so the web-facing ports can be bound to a chosen host interface while discovery/adoption ports remain published normally. Set `OMADA_BIND_IP` to the host interface that should expose ports `8043`, `8088`, and `8843`. Leave it empty to use Docker's default all-interface binding.

The upstream image recommends host networking as the easiest option for discovery and adoption. If devices cannot discover a bridge-mode controller, either configure the controller address on the devices or adapt this template to `network_mode: host`.

Published discovery/management ports follow the current upstream v6 example, including UDP `19810`, `27001`, and `29810`, plus TCP `29811-29817`.

## Versioning

Do not switch this image to `latest`. Upstream intentionally keeps `latest` on the v5 line because upgrading from v5 to v6 requires a manual MongoDB migration. The `6.2` major/minor tag is the recommended stable update track for v6.

If upgrading an existing v5 controller, follow the upstream v5-to-v6 migration guide before changing the image tag.

## Persistence

| Variable | Default | Purpose |
| --- | --- | --- |
| `DATA_DIR` | `./data` | Controller database and configuration |
| `LOGS_DIR` | `./logs` | Controller logs |
| `TZ` | `Etc/UTC` | Container timezone |
| `OMADA_BIND_IP` | all interfaces | Host interface used for web/portal ports |
| `OMADA_VERSION` | `6.2` | Omada image update track |

The 60-second stop grace period and increased `nofile` limits match upstream operational recommendations and help the embedded database shut down cleanly.
