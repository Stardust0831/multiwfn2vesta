# Skill: VESTA CLI from WSL through Windows interop

## When to use

Use this workflow when the Windows VESTA executable must be controlled from WSL
to save `.vesta` files or export PNG images.

## Known executable

```text
/mnt/g/work/multiwfn2vesta/tools/VESTA-win64/VESTA.exe
```

Windows path:

```text
G:\work\multiwfn2vesta\tools\VESTA-win64\VESTA.exe
```

## Rules

- Convert file paths with `wslpath -w`.
- Quote each executable and file path argument separately.
- Use `timeout`; VESTA often exports output but does not exit cleanly.
- Always run cleanup after export.
- Treat VESTA nonzero exit codes cautiously; check whether output files exist.

## Good command pattern

```bash
IN=$(wslpath -w input.vesta)
OUT=$(wslpath -w output.png)
VESTA='G:\work\multiwfn2vesta\tools\VESTA-win64\VESTA.exe'

timeout 30s /mnt/c/WINDOWS/system32/cmd.exe /c "$VESTA" \
  -open "$IN" \
  -export_img scale=1 "$OUT" \
  -flush -close

/mnt/c/WINDOWS/system32/cmd.exe /c "$VESTA" -close || true
```

## Bad pattern

Avoid putting the full command and unquoted Windows paths inside one large
`cmd /C "..."` string. In local experiments this caused absolute paths to be
misread as relative paths such as `smoke\...`, and VESTA could not save output.

## Output validation

```bash
file output.png
file output.vesta
```

For parser validation:

```bash
PYTHONPATH=project/src python - <<'PY'
from pathlib import Path
from multiwfn2vesta.vesta_parser import read_vesta_bytes
p = Path("output.vesta")
d = read_vesta_bytes(p)
print(d.to_bytes() == p.read_bytes())
PY
```

