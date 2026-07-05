"""PyInstaller entry point for the user-facing multiwfn2vesta CLI."""

from multiwfn2vesta.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
