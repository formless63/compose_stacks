# compose_stacks

A collection of personal Docker Compose stacks.

> **Note:** These examples are current as of the commit date. Always check the official documentation for the specific service you are deploying to ensure you have the latest configuration changes.

## Getting Started

If you are new to Docker Compose, review the basics before deploying these stacks:

* [Docker Compose Getting Started](https://docs.docker.com/compose/gettingstarted/) (Official Docs)
* [Docker Compose Tutorial](https://adamtheautomator.com/docker-compose-tutorial/) (AdamTheAutomator)

## Recommended Management Tools

While CLI is standard, using a GUI can simplify stack management. Many of these tools can pull directly from this repository:

| Name | Website | GitHub |
| --- | --- | --- |
| **Komodo** | [komo.do](https://komo.do/) | [moghtech/komodo](https://github.com/moghtech/komodo) |
| **Dockhand** | [dockhand.pro](https://dockhand.pro/) | [Finsys/dockhand](https://github.com/Finsys/dockhand) |

## Usage

1. Navigate to the directory of the stack you want to use.
2. Copy `.env.example` to `.env`.
3. Edit `.env` to match your environment variables (paths, ports, PUID/PGID).
4. Run `docker compose up -d`.
