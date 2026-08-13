# compose_stacks

A collection of reusable Docker Compose templates for self-hosted services.

> These are deployment templates, not upstream release manifests. Review the linked upstream documentation before major-version upgrades, especially for stateful services.

## Repository layout

Each active stack lives in its own top-level directory. Keep stack-specific files local to that directory so Git-backed deployment tools can treat it as a self-contained deployment unit.

```text
stack-name/
├── compose.yaml
├── .env.example        # when configuration is needed
├── README.md
└── supporting files    # optional; configs, scripts, etc.
```

Use `compose.yaml` as the standard filename for the primary deployment. If a service genuinely needs multiple deployment variants, keep the default in `compose.yaml` and name alternatives descriptively, such as `compose.external-db.yaml`.

## Stacks

| Stack | Compose path |
| --- | --- |
| BitMappery | `bitmappery/compose.yaml` |
| Directus | `directus/external-db-compose.yaml` |
| Omada Controller | `omada/compose.yaml` |
| Penpot | `penpot/compose.yaml` |
| Portabase | `portabase/compose.yml` |
| Portabase Agent | `portabase-agent/compose.yml` |
| ReadMeABook | `readmeabook/compose.yaml` |
| Storyteller | `storyteller/compose.yaml` |
| Super Productivity | `super-productivity/compose.yaml` |

Retired examples are kept under `.retired/` and are not part of the active template set.

## CLI usage

```bash
git clone https://github.com/formless63/compose_stacks.git
cd compose_stacks/<stack>
cp .env.example .env   # when the stack has an env example
# edit .env
docker compose up -d
```

Never commit a populated `.env` or other deployment secrets.

## Dockhand Git stacks

This repository's one-directory-per-stack layout maps directly to Dockhand Git stacks:

1. Add this repository in Dockhand's Git settings.
2. Create a Git-backed stack and select the desired branch.
3. Set **Compose file path** to the path in the table above, for example `omada/compose.yaml`.
4. Leave **Context directory** unset for self-contained stacks. Set it only if a compose file intentionally references files outside its own directory.
5. Put host-specific values in Dockhand's environment overrides rather than modifying the reusable template.

Dockhand monitors the compose directory for Git changes, so a commit to one stack does not need to redeploy unrelated stacks in this repository.

## Maintenance

Compose syntax is validated by GitHub Actions. Image/version updates should be reviewed against each project's official release notes and upgrade instructions rather than switching stateful applications to `latest` indiscriminately.

## Management tools

- [Dockhand](https://dockhand.pro/) — Git-backed Compose stack management
- [Komodo](https://komo.do/) — infrastructure and Compose management
