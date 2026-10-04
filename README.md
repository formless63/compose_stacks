# Tested Docker Compose stacks

Community deployment examples for BitMappery, Super Productivity / SuperSync, Penpot, Directus, Portabase and its agent, Storyteller, and ReadMeABook. These are independent stacks; deploy only the ones you need.

| Stack | Purpose | Setup |
| --- | --- | --- |
| BitMappery | Browser image editor | [Guide](bitmappery/README.md) |
| Super Productivity / SuperSync | Productivity app and device sync | [Guide](super-productivity/README.md) |
| Penpot | Collaborative design | [Guide](penpot/README.md) |
| Directus | Data platform with external PostgreSQL | [Guide](directus/README.md) |
| Portabase | Database backup dashboard | [Guide](portabase/README.md) |
| Portabase agent | Remote database backup agent | [Guide](portabase-agent/README.md) |
| Storyteller | Ebooks with synchronized audiobook narration | [Guide](storyteller/README.md) |
| ReadMeABook | Audiobook requests and library management | [Guide](readmeabook/README.md) |

Run commands from the selected stack directory. Copy its environment example, edit URLs, secrets, permissions and storage paths, then check `docker compose config --quiet` before launching. Directus uses explicit filenames: see its guide. Required empty settings fail with a useful error. Examples are templates, not production credentials.

Published ports bind all host interfaces by default unless an address is specified. Configure your firewall or supply a loopback/interface address in the port setting where supported. Services using secure cookies or passkeys need HTTPS through your reverse proxy. External networks are documented per stack.

## Validation

[VALIDATION.md](VALIDATION.md) records what was actually tested, exact image identities and remaining limitations. Configuration validation is separate from startup and functional validation. Files in `.retired/` are archived examples and are excluded from active checks.

```sh
python3 scripts/validate.py
python3 scripts/smoke.py bitmappery
```

The first command resolves all eight active stacks and checks required-variable failures without starting services. CI runs it for pushes and pull requests. A separate manual/weekly workflow runs the seven disposable application smoke tests and retains their image identities and logs. The second creates a disposable test project with fresh named volumes and random loopback ports; it never reads deployment `.env` files or mounts deployment data. It cleans up its own resources afterwards. Other supported smoke targets are `super-productivity`, `penpot`, `directus`, `portabase`, `storyteller`, and `readmeabook`. The agent requires an actual dashboard registration and disposable database backup/restore; it has configuration validation only here.

Smoke tests use public fixture secrets, an isolated mail sink for Penpot, and a disposable external database for Directus. They check the application response and persistence through a restart. They do not cover every integration or establish production upgrade safety. `--image SERVICE=IMAGE` selects a local image for an individual service.

## Updates and backups

Pin a tested release or immutable digest where practical. Floating `latest` tags can change between pulls; save the running digest before upgrading. Keep application images in multi-service stacks on a matching release. Existing database major versions and bind paths are preserved; changing a database image's major version requires a deliberate data migration.

Back up databases with supported tools and retain application files and secrets. Test restoration. Consult each guide for migration ordering, especially SuperSync. No stack should be updated against live data merely to validate this repository.

[Komodo](https://komo.do/) and [Dockhand](https://dockhand.pro/) can help manage deployments; Docker Compose CLI remains supported.
