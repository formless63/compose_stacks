# qBittorrent + Gluetun + Dashboards

qBittorrent behind ProtonVPN WireGuard, with Gluetun WebUI for VPN status and controls and qbit_manage for configuring torrent management through a browser. All four services are included.

**Links:**
* [Gluetun](https://github.com/qdm12/gluetun) · [Container](https://hub.docker.com/r/qmcgaw/gluetun)
* [Binhex qBittorrent](https://github.com/binhex/arch-qbittorrent) · [Container](https://hub.docker.com/r/binhex/arch-qbittorrent)
* [Gluetun WebUI](https://github.com/Sir-Scuzza/gluetun-webui) · [Container](https://hub.docker.com/r/scuzza/gluetun-webui)
* [qbit_manage](https://github.com/StuffAnThings/qbit_manage) · [Web UI guide](https://github.com/StuffAnThings/qbit_manage/blob/master/docs/Web-UI.md)

## Quick Start

1. **Get the Repository**
```bash
   git clone https://github.com/formless63/compose_stacks.git
   cd compose_stacks/qbittorrent-gluetun
```

2. **Prepare Environment**
```bash
cp .env.example .env
```

3. **Edit Configuration**
```bash
nano .env
```

* Set `PROTON_KEY` to a Proton WireGuard private key generated with **NAT-PMP (Port Forwarding)** enabled. This setup requires a plan supporting port forwarding and a Linux Docker host with `/dev/net/tun`.
* Set strong `GLUETUN_PASS` and `QBIT_PASS` passwords. Use alphanumeric characters for `GLUETUN_PASS`, because Gluetun's authentication setting is JSON.
* Set `PUID` / `PGID` to your host user (run `id`) and update the `_DIR` paths. Keep download paths identical for both applications.
* Dashboards default to localhost: ports `3009` and `8185`. For a trusted home LAN, set `VPN_UI_BIND_IP` and `MANAGE_BIND_IP` to the Docker host's LAN address. Gluetun WebUI has **no built-in login**; its Gluetun credentials protect the upstream API, not the dashboard. For wider access use an authenticated reverse proxy. Enable qbit_manage authentication in its Security settings before exposing it.
* Initialize qbit_manage's editable configuration once (replace the path below if you changed `MANAGE_CONFIG_DIR`):
```bash
mkdir -p ./config/qbit_manage
cp -n qbit-manage.example.yml ./config/qbit_manage/config.yml
```
* **Save & Exit:** Press `Ctrl+X`, then `Y`, then `Enter`.

4. **Launch**
```bash
docker compose up -d
```

5. **Verify**
```bash
docker compose logs -f
```

*(Press `Ctrl+C` to exit logs.)*

Open qBittorrent at `http://YOUR_HOST:8080`, Gluetun WebUI at `http://localhost:3009`, and qbit_manage at `http://localhost:8185` when browsing on the Docker host. Use the host's LAN address for dashboards if you changed their bind addresses. Log into qBittorrent using `QBIT_USER` / `QBIT_PASS`.

In qbit_manage select `config.yml` and configure categories, trackers, share limits and other rules through the UI. The starter already points to `gluetun:8080` and uses your `.env` credentials. Leave **Dry Run** enabled until you have reviewed the rules and logs. Container settings such as ports and mounted directories remain in `.env`.

## Configuration

| Variable | Description | Default | Recommendation |
| --- | --- | --- | --- |
| `GLUETUN_IMAGE` / `QBIT_IMAGE` / `VPN_UI_IMAGE` / `MANAGE_IMAGE` | Container selections | Respective upstream `latest` | Pin a tested tag or digest in `.env` |
| `PROTON_KEY` | WireGuard private key | Required | Generate with NAT-PMP enabled |
| `GLUETUN_USER` / `GLUETUN_PASS` | Internal control API credentials | `gluetun` / required | Long alphanumeric password |
| `QBIT_USER` / `QBIT_PASS` | qBittorrent credentials | `admin` / required | Keep existing installations' stored credentials aligned |
| `SERVER_COUNTRIES` | Proton server country filter | `United States` | Select a supported country |
| `QBIT_PORT` / `VPN_UI_PORT` / `MANAGE_PORT` | Host UI ports | `8080` / `3009` / `8185` | Change if already used |
| `QBIT_BIND_IP` | qBittorrent host binding | `0.0.0.0` | Use host LAN IP for narrower access |
| `VPN_UI_BIND_IP` / `MANAGE_BIND_IP` | Dashboard host bindings | `127.0.0.1` | Set LAN IP for trusted LAN access |
| `FIREWALL_OUTBOUND_SUBNETS` | Destinations accessible outside VPN | Empty | Add only needed host IPs or narrow subnets |
| `PUID` / `PGID` / `UMASK` | File permissions | `1000` / `1000` / `002` | Match the host account |
| `VPN_CONFIG_DIR` / `QBIT_CONFIG_DIR` / `MANAGE_CONFIG_DIR` | Persistent configuration | Under `./config` | Keep when updating |
| `DOWNLOADS_DIR` | Shared download storage | `./downloads` | Same mount path for both apps |
| `MANAGE_SCHEDULE` | Scheduler interval, minutes | `1440` | Configure for your needs |

See [networking, updates and validation notes](../.resources/maintenance/qbittorrent-gluetun.md).
