# Project Packaging And UX Rules

## Stable vs Experimental

Stable tools must have at least one of:

- committed tests,
- committed sample input/output files,
- a user-confirmed real workflow that was recorded in docs/kanban or a skill.

Experimental workflows can remain in `docs/skills/`, `docs/research/`, or
low-level CLI commands, but should not appear in the stable `tools` list.

## CLI Language

Human-facing tool discovery supports:

```bash
multiwfn2vesta --lang zh
multiwfn2vesta tools --lang zh
multiwfn2vesta tools --lang en
multiwfn2vesta tools interactive --lang zh
```

Keep low-level scriptable commands stable and mostly English so existing
automation does not break. Add Chinese text primarily to the high-level tools
layer, manuals, and examples.

## Distribution

Preferred default:

- Python package/console scripts.
- No system-level installation requirement.
- Workspace-local `bin/` launcher remains acceptable.

GitHub Actions/release packaging is allowed when:

- entry points stay explicit,
- generated executables are reproducible,
- external binaries such as Multiwfn/VESTA are not silently bundled unless
  license and platform constraints are documented,
- release notes clearly separate stable tools from experimental runbooks.

## Documentation Sync

When adding a stable tool:

1. Add it to `src/multiwfn2vesta/tools.py`.
2. Add tests.
3. Update `README.md`, `docs/manual_zh.md`, and
   `docs/skills/multiwfn2vesta_cli_skill.md`.
4. Update this skill's `references/stable_tools.md`.
5. Record the change in `docs/kanban.md`.
