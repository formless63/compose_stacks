# Validation record

Validated on 2026-10-04 using Docker 28.4.0 and Compose 2.40.3 on Linux AMD64.
[Exact image IDs, registry digests and source revisions](results.json).

Following the template correction, all nine stacks were checked again with environment-selected images. Penpot, SuperSync and Omada functional tests were rerun successfully; the remaining application evidence below comes from the preceding maintenance pass with the same default images. Container names and logging limits are now configurable, and validation tools/results live entirely under `.resources/`.

## Completed checks

- All ten active stacks resolved successfully using `python3 .resources/validation/validate.py`, with no interpolation warnings.
- 29 checks confirmed that empty required settings fail with an explanatory message.
- All application/database image selections were overridden through fixture environment values and confirmed in the resolved models, proving that `.env` choices take effect.
- Portabase's optional proxy overlay resolved successfully.
- Both GitHub workflows passed actionlint 1.7.12. ShellCheck was unavailable locally; actionlint's ShellCheck integration was disabled for that local run.
- Python validation/smoke helpers compiled, and `git diff --check` passed.

| Stack | Functional evidence |
| --- | --- |
| qBittorrent + Gluetun + dashboards | Gluetun dashboard HTML and authenticated simulated-control health passed with a read-only filesystem; qbit_manage loaded, edited and saved the starter configuration through its API, preserving `!ENV` credentials. Live VPN and torrent integration were not tested. |
| Omada 6.2 | Controller setup HTML served over HTTPS with its generated certificate trusted only for the disposable test; controller data survived restart. LAN adoption was not tested. |
| BitMappery | HTML application, compiled JavaScript asset, SPA fallback. No persistent service data required. |
| Super Productivity / SuperSync | All 29 migrations applied against disposable PostgreSQL 15, healthy API with connected database, web frontend served HTML, application data survived server restart. |
| Penpot 2.18.1 | Full stack started with PostgreSQL 15, Valkey and isolated mail sink; anonymous-profile backend RPC succeeded through nginx; actual exporter Chromium rendered and inspected a local page; shared assets volume survived frontend restart. |
| Directus | Disposable external PostgreSQL and Redis 8 started; public ping, administrator login and authenticated database health succeeded; uploads volume survived app restart. |
| Portabase | Dashboard health succeeded with disposable PostgreSQL 17; application data survived app restart. |
| Storyteller | Application HTML served using configured AUTH_URL; data volume survived app restart. |
| ReadMeABook | Unified-container health succeeded with bundled database/cache; configuration volume survived app restart. |
| Portabase agent | Compose and required-variable validation passed; JSON example and runtime setting names checked against upstream source. Registration and backup/restore were not run. |

All smoke containers, project networks and test volumes were removed afterwards. Test fixtures did not read deployment `.env` files or mount deployment data. Named test volumes preserve image-provided ownership; bind-directory permissions remain a deployment prerequisite, documented explicitly for SuperSync, Penpot and Directus. Penpot UID/GID 1001 was confirmed from the tested image; SuperSync UID/GID 1001 matches its upstream Dockerfile. The smoke runner preserves shared bind-source relationships as shared disposable volumes.

## Cloud adaptations and limits

This environment uses Docker's VFS storage driver with a 32 GB filesystem. Normal pulls of large multi-layer images exceeded that limit. Omada, ReadMeABook, Storyteller, Portabase, Directus and the five Penpot application images were exported from immutable upstream registry references using checksum-verified crane 0.22.1, then imported locally as single-layer filesystems. Upstream entrypoint, command, environment, working directory, user, ports, volumes and labels were restored; explicit Compose health checks were retained. The record lists both the upstream reference and the local test image ID. Published Compose definitions still use normal upstream images. Initial disk-limited runs were retried after deleting unused test image caches; the table records completed successful runs.

BitMappery and SuperSync used the locally built companion images from the docker-builds maintenance work, rather than asserting that a particular public `latest` tag already contains those changes. See that repository's validation record for its build adaptations. The other application images were pulled/exported from their upstream registries. Redis was pinned to the currently published major version 8 to avoid a cache downgrade from the previous `latest` default. Native ARM64 runs and GitHub-hosted CI execution have not been performed here.

These checks establish fresh deployment behavior and selected application paths. They do not establish production database upgrade/rollback safety, email delivery, passkey enrollment, external OAuth, media import/alignment, downloader integration, full Penpot document export, or real backup/restore. Those require representative data and integrations. The agent needs a dashboard-issued key and disposable database for its remaining integration check. Storyteller's public documentation website returned HTTP 403 here; its current GitLab README and image were accessible.

## Repeat

```sh
python3 .resources/validation/validate.py
python3 .resources/validation/smoke.py STACK
```

Run one large stack at a time on storage-limited hosts. Smoke tests create their own resources and clean them up. `--image SERVICE=IMAGE` allows testing a local image; use the same image for both SuperSync's server and migration job. The standard smoke workflow runs each application in a separate GitHub runner, manually or weekly, and uploads its results. The agent is intentionally excluded from unattended functional checks that would require real registration credentials.

## qBittorrent dashboard checks

The new VPN stack keeps both dashboards included. All ten stacks resolved after its addition; 29 required-variable failure checks passed. Networking assertions check shared Gluetun networking, no published control API, empty outbound LAN exceptions and localhost dashboard defaults. The dashboard tests used upstream images directly:

- `scuzza/gluetun-webui@sha256:a7c2b4c77f26bb690debe6879cd7149d69710578b13e0dcdc08f6b9b6c7a7a14`
- `ghcr.io/stuffanthings/qbit_manage@sha256:ea04167f627e506b3691304f4c639a52c05584cc9aea4af7ec87d4ed1299e7f5`

Repeat these focused UI checks without Proton credentials:

```sh
docker pull scuzza/gluetun-webui:latest
docker pull ghcr.io/stuffanthings/qbit_manage:latest
python3 .resources/validation/qbittorrent_dashboards.py
```

The control API is simulated with HTTP Basic authentication. The qbit_manage scheduler is delayed so tests cannot operate on torrents. All configuration and downloads use temporary test directories; all test containers and the network are removed afterwards. These checks do not test Gluetun's actual firewall, Proton authentication/NAT-PMP, qBittorrent credential initialization or forwarded-port updates, or torrent-management rules against a live client. The VPN stack is excluded from unattended full-stack smoke runs because it requires a suitable Proton account and VPN network access.
