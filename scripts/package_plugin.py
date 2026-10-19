"""Validate and create a reproducible distributable ZIP from plugin components."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
from validate_plugin import validate

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'dist' / 'byui-brand-guide-plugin.zip'
INCLUDE = ('plugin.json', '.codex-plugin', 'skills', 'assets')


def main():
    errors = validate(ROOT)
    if errors:
        raise SystemExit('\n'.join(errors))
    OUTPUT.parent.mkdir(exist_ok=True)
    with ZipFile(OUTPUT, 'w', ZIP_DEFLATED, compresslevel=6) as archive:
        for name in INCLUDE:
            source = ROOT / name
            files = sorted(source.rglob('*')) if source.is_dir() else [source]
            for path in files:
                if '__pycache__' in path.parts or path.name == '.DS_Store' or path.suffix == '.pyc':
                    continue
                if path.is_symlink():
                    raise ValueError(f'Symlinks are not plugin content: {path}')
                if path.is_file():
                    info = ZipInfo(str(Path('byui-brand-guide') / path.relative_to(ROOT)), (2020, 1, 1, 0, 0, 0))
                    info.compress_type = ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, path.read_bytes(), compresslevel=6)
    with ZipFile(OUTPUT) as archive:
        if archive.testzip() is not None:
            raise SystemExit('Generated archive integrity failed')
    print(OUTPUT)


if __name__ == '__main__':
    main()
