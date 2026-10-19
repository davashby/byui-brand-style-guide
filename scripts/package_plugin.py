"""Create a distributable plugin ZIP from the tracked source files."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist" / "byui-brand-guide-plugin.zip"
INCLUDE = ("plugin.json", ".codex-plugin", "skills", "assets")


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for name in INCLUDE:
            source = ROOT / name
            files = sorted(source.rglob("*")) if source.is_dir() else [source]
            for path in files:
                if path.is_file() and path.name != ".DS_Store":
                    archive.write(path, Path("byui-brand-guide-plugin") / path.relative_to(ROOT))
    print(OUTPUT)


if __name__ == "__main__":
    main()
