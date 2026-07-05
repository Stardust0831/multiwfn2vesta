---
name: multiwfn2vesta-operator
description: Operate and maintain the multiwfn2vesta project for stable Multiwfn, ABACUS, and VESTA workflows. Use when Codex needs to choose human-facing tools, package only tested workflows, update project records/kanban, generate VESTA scenes, interpret .vesta fields, or preserve user-approved Multiwfn/VESTA/ABACUS practices.
---

# multiwfn2vesta Operator

Use the stable tool layer before reaching for low-level commands. Keep
experimental routes as runbooks until they have tests or user-confirmed
working examples.

## Required Project Habits

1. Write every new user request into `docs/kanban.md` before implementation.
2. Keep all local edits under `/mnt/g/work/multiwfn2vesta`.
3. Do not revert unrelated dirty files; inspect and stage only task-relevant
   paths.
4. Prefer `multiwfn2vesta tools` for human-facing workflows and low-level
   commands for debugging.
5. Mark only tested or explicitly user-approved workflows as stable.
6. When VESTA rendering is involved, separate `.vesta` generation from GUI PNG
   rendering unless the user explicitly asks to render.

## Stable Tool Layer

Run:

```bash
multiwfn2vesta tools --lang zh
multiwfn2vesta tools interactive --lang zh
multiwfn2vesta tools run <tool> -- <args>
```

Read `references/stable_tools.md` when deciding which high-level tool to use.
If a request maps to a stable tool, use it. If it needs an experimental
workflow, say it is experimental and use the lower-level runbook.

## VESTA Files

Read `references/vesta_file_format.md` before editing `.vesta` fields,
debugging missing bonds/labels/texture colors, copying camera views, or
interpreting `STRUC`, `SITET`, `SBOND`, `SCENE`, `ISURF`, `TEX3P`, `BOUND`,
`PHASON`, or `QCORIG`.

Rules:

- Preserve unknown directives and whitespace whenever possible.
- Treat `TEX3P` as VESTA percentage/normalized texture range, not physical
  scalar values.
- Structure bonds need both global `BONDS` and nonempty `SBOND` rules.
- AIM path/BCP phases should normally have empty `SBOND` to avoid fake bonds.
- Do not move AIM/BCP coordinates to fix a view problem; adjust the view.

## Packaging Guidance

Read `references/project_packaging.md` when changing CLI, release, or skill
structure. The default package goal is a clear Python CLI with no system-level
changes. GitHub Actions or bundled executables are allowed only when they keep
entry points explicit and do not promote experimental workflows as stable.
