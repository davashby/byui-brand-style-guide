"""Make a working PPTX from a supplied anniversary template without flattening parts."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_TYPE = b'application/vnd.openxmlformats-officedocument.presentationml.template.main+xml'
PRESENTATION_TYPE = b'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'


def prepare(variant, output, anniversary_approved=False):
    if not anniversary_approved:
        raise ValueError('Current anniversary authorization must be confirmed before using these templates. Obtain an approved generic template for other uses.')
    if variant not in ('blue', 'white'):
        raise ValueError('Variant must be blue or white')
    output = Path(output)
    if output.suffix.lower() != '.pptx':
        raise ValueError('Output must end in .pptx')
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite {output}')
    catalog = json.loads((ROOT / 'assets/catalog.json').read_text())
    suffix = f'BYUI_{variant.title()}_Template.potx'
    record = next(a for a in catalog['assets'] if a['path'].endswith(suffix))
    source = ROOT / record['path']
    if hashlib.sha256(source.read_bytes()).hexdigest() != record['sha256']:
        raise ValueError('Template hash does not match the catalog; revalidate the source.')
    with ZipFile(source) as original:
        if original.testzip() is not None:
            raise ValueError('Template ZIP integrity failed')
        content_types = original.read('[Content_Types].xml')
        if content_types.count(TEMPLATE_TYPE) != 1:
            raise ValueError('Expected exactly one template main content type')
        content_types = content_types.replace(TEMPLATE_TYPE, PRESENTATION_TYPE)
        output.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(output, 'x') as result:
            for item in original.infolist():
                result.writestr(item, content_types if item.filename == '[Content_Types].xml' else original.read(item.filename))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--variant', choices=['blue', 'white'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--anniversary-approved', action='store_true', help='Use only after independently confirming current authorization; this flag does not grant approval.')
    args = parser.parse_args()
    try:
        result = prepare(args.variant, args.output, args.anniversary_approved)
    except (ValueError, FileExistsError) as exc:
        parser.error(str(exc))
    print(f'{result.resolve()}\nWorking copy retains anniversary artwork and examples. Validate all subsequent edits and exports.')


if __name__ == '__main__':
    main()
