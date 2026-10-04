# compose_stacks

A public collection of Docker Compose stacks that have been tested for self-hosting.

## Getting Started

1. Choose a stack below and open its setup guide.
2. Copy its `.env.example` to `.env` (Directus uses `external-db-.env.example`).
3. Edit `.env` for your host: image versions, URLs, ports, secrets and data paths.
4. Run `docker compose up -d` from the stack directory. Directus's guide includes its explicit filename.

Keep your `.env` and data when pulling updates. Read the stack's update notes before changing application or database versions.

## Stacks

| Stack | Compose file | Guide |
| --- | --- | --- |
| BitMappery | `bitmappery/compose.yaml` | [Setup](bitmappery/README.md) |
| Super Productivity | `super-productivity/compose.yaml` | [Setup](super-productivity/README.md) |
| Penpot | `penpot/compose.yaml` | [Setup](penpot/README.md) |
| Directus | `directus/external-db-compose.yaml` | [Setup](directus/README.md) |
| Portabase | `portabase/compose.yml` | [Setup](portabase/README.md) |
| Portabase agent | `portabase-agent/compose.yml` | [Setup](portabase-agent/README.md) |
| Storyteller | `storyteller/compose.yaml` | [Setup](storyteller/README.md) |
| ReadMeABook | `readmeabook/compose.yaml` | [Setup](readmeabook/README.md) |
| Omada Controller | `omada/compose.yaml` | [Setup](omada/README.md) |

## Management Tools

* [Dockhand](https://dockhand.pro/) — use the Compose path above for a Git-backed stack, and set host values in its environment overrides.
* [Komodo](https://komo.do/) — infrastructure and Compose stack management.

## Repository Layout

Each stack has its own directory with a Compose file, environment example and README. Supporting material stays under `.resources/`: [templates](.resources/templates), [maintenance notes](.resources/maintenance), and [validation results and tools](.resources/validation/README.md). Retired stacks are in `.retired/`.

For new stacks, follow `.resources/templates`, use `compose.yaml`, and register the stack in the validation tool. Existing filenames are preserved for compatibility.
