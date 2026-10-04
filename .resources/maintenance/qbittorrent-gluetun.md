# qBittorrent + Gluetun maintenance

## Firewall and network access

qBittorrent uses `network_mode: service:gluetun`. Its published WebUI port lives on Gluetun; do not add a separate qBittorrent network or host-published torrent port. Binhex reads Proton's forwarded port through Gluetun's authenticated control API and updates qBittorrent automatically. There is no tracker-specific script hook.

`FIREWALL_OUTBOUND_SUBNETS` defaults to empty. Receiving a browser request is different from initiating an outbound LAN connection: dashboards reach Gluetun through the shared Docker bridge, with inbound management ports `8080,8000` explicitly allowed. The control API remains unpublished on the host. Reply traffic to incoming requests does not require allowing every private subnet.

If qBittorrent must initiate a connection to a local service, add that service's IP, e.g. `192.168.1.50/32`, or the smallest appropriate LAN subnet. This traffic bypasses the VPN intentionally. Do not copy blanket `10.0.0.0/8`, `172.16.0.0/12` or `192.168.0.0/16` exceptions. Do not overlap the VPN tunnel subnet: Proton NAT-PMP traffic can be routed away from the tunnel and port forwarding can fail. See [Gluetun firewall documentation](https://github.com/qdm12/gluetun-wiki/blob/main/setup/options/firewall.md).

The dashboards have normal Docker networking; only qBittorrent's traffic is routed through the VPN. qbit_manage can therefore contact configured notification services outside the VPN.

## First run and credentials

The qbit_manage Web UI is a configuration editor. Copy the small example into your persistent configuration directory once, then use the UI. The upstream entrypoint copies a `.sample` file, not an active `config.yml`. Never overwrite an existing user configuration when pulling updates. The starter disables management actions and enables dry-run; customize it before enabling scheduled changes.

Binhex initializes qBittorrent's password from `QBIT_PASS` only when no existing configuration is present. On subsequent runs, this environment value is used by port-forward automation; it does not replace the password saved by qBittorrent. Change an existing password through qBittorrent's UI and update `.env` to match, then recreate the containers. qbit_manage's connection uses the same credentials unless you change them in its UI.

Gluetun WebUI's `GLUETUN_USER` and `GLUETUN_PASSWORD` authenticate its server-side requests to Gluetun; they do not add a dashboard login. Keep it on localhost or a trusted LAN, or protect it with reverse-proxy authentication. qbit_manage has authentication configurable in its Security UI.

## Updates and recovery

Back up `.env`, all configuration directories, and data you need before upgrading. Pin image tags or digests in `.env` to keep image choices stable across repository updates. Updating this Git repository preserves `.env` and the copied qbit_manage configuration.

When updating/recreating Gluetun, recreate qBittorrent too so it attaches to the new network namespace:

```bash
docker compose pull
docker compose up -d --force-recreate
```

A VPN reconnect within the existing Gluetun container is different from replacing that container. Verify the forwarded port and qBittorrent connectivity after either event. Gluetun's firewall is the protection during VPN outages; Compose's healthy dependency gates initial startup, not continuous VPN health.

## Validation scope

The submitted stack was reported by its owner to have run locally for a week. Repository validation checks all four services, environment interpolation and image overrides, required credentials, shared VPN networking, unpublished control API, default dashboard bindings, and the empty outbound exception list. Cloud dashboard checks do not establish Proton connectivity, disconnect protection, NAT-PMP port changes, or end-to-end qbit_manage operation against a live qBittorrent/VPN deployment. Those require validation on a Linux host with a suitable Proton account.
