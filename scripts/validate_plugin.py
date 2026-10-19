"""Validate the portable manifest, asset inventory, links, and Office package parts."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from posixpath import join, normpath
from urllib.parse import unquote
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent


def check_schema(value, schema, location='$'):
    """Apply the keywords used by the vendored, official Agent Plugins 1.0 schema."""
    errors = []
    types = {'object': dict, 'array': list, 'string': str}
    if 'type' in schema and not isinstance(value, types[schema['type']]):
        return [f'{location}: expected {schema["type"]}']
    if 'const' in schema and value != schema['const']:
        errors.append(f'{location}: unexpected constant')
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0) or len(value) > schema.get('maxLength', float('inf')):
            errors.append(f'{location}: string length outside schema bounds')
        if 'pattern' in schema and re.search(schema['pattern'], value) is None:
            errors.append(f'{location}: pattern mismatch')
    if isinstance(value, dict):
        props = schema.get('properties', {})
        errors += [f'{location}: missing {key}' for key in schema.get('required', []) if key not in value]
        for key, child in value.items():
            if key in props:
                errors += check_schema(child, props[key], f'{location}.{key}')
            elif schema.get('additionalProperties') is False:
                errors.append(f'{location}: disallowed property {key}')
            elif isinstance(schema.get('additionalProperties'), dict):
                errors += check_schema(child, schema['additionalProperties'], f'{location}.{key}')
    if isinstance(value, list) and 'items' in schema:
        for i, child in enumerate(value):
            errors += check_schema(child, schema['items'], f'{location}[{i}]')
    return errors


def contained(root, path):
    root = Path(root).resolve()
    result = (root / path).resolve()
    if not result.is_relative_to(root):
        raise ValueError(f'Path escapes plugin root: {path}')
    return result


def office_errors(path):
    errors = []
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            errors.append(f'{path.name}: ZIP integrity failure')
        names = set(archive.namelist())
        for name in names:
            if name.endswith(('.xml', '.rels')):
                ET.fromstring(archive.read(name))
            if name.endswith('.rels'):
                base = '' if name == '_rels/.rels' else name.rsplit('/_rels/', 1)[0]
                for rel in ET.fromstring(archive.read(name)):
                    if rel.get('TargetMode') == 'External':
                        continue
                    target = rel.get('Target', '').split('#', 1)[0]
                    if target and normpath(join(base, unquote(target))).lstrip('/') not in names:
                        errors.append(f'{path.name}: missing internal target {target}')
    return errors


def validate(root=ROOT):
    root = Path(root).resolve()
    manifest = json.loads((root / 'plugin.json').read_text())
    legacy = json.loads((root / '.codex-plugin/plugin.json').read_text())
    schema = json.loads((ROOT / 'scripts/schemas/agent-plugins-1.0.0.json').read_text())
    errors = check_schema(manifest, schema)
    interface = manifest['extensions']['com.openai']['interface']
    for field in ['name', 'version', 'description', 'author', 'repository', 'keywords']:
        if manifest[field] != legacy[field]:
            errors.append(f'Manifest mismatch: {field}')
    if interface != legacy['interface']:
        errors.append('Manifest interface mismatch')
    if not re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']):
        errors.append('Expected strict release semantic version')
    if len(interface['shortDescription']) > 30:
        errors.append('Listing subtitle exceeds 30 characters')
    for key in ['logo', 'logoDark', 'composerIcon', 'composerIconDark']:
        value = interface.get(key)
        if not value or not value.startswith('./') or not contained(root, value).is_file():
            errors.append(f'Invalid icon reference: {key}')
    for key in ['brandColor', 'brandColorDark']:
        if re.fullmatch(r'#[0-9A-Fa-f]{6}', interface[key]) is None:
            errors.append(f'Invalid {key}')
    catalog = json.loads((root / 'assets/catalog.json').read_text())
    indexed = set()
    for record in catalog['assets']:
        path = contained(root, record['path']); indexed.add(path)
        if not path.is_file():
            errors.append(f'Missing asset: {record["path"]}'); continue
        if path.stat().st_size != record['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            errors.append(f'Asset differs from validated inventory: {record["path"]}')
        if path.suffix in ('.docx', '.potx'):
            errors += office_errors(path)
        if path.suffix == '.svg':
            ET.parse(path)
        if record.get('contains_anniversary_master_footer') and (record.get('requires_current_authorization') is not True or record.get('campaign') != '25-year-anniversary'):
            errors.append(f'Anniversary template lacks restriction: {record["path"]}')
    actual = {p.resolve() for p in (root / 'assets').rglob('*') if p.is_file() and p.suffix != '.json'}
    if actual != indexed:
        errors.append('Asset inventory does not match package assets')
    layout_index = json.loads((root / 'assets/powerpoint-layouts.json').read_text())
    for row in layout_index['templates']:
        path = contained(root, row['path'])
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            errors.append(f'Stale layout index: {row["path"]}')
        with ZipFile(path) as archive:
            layouts = row.get('layouts', layout_index.get('layout_sets', {}).get(row.get('layout_set'), []))
            actual_parts = {n for n in archive.namelist() if re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', n)}
            if {layout['part'] for layout in layouts} != actual_parts:
                errors.append(f'Incomplete layout index: {row["path"]}')
    for md in (root / 'skills').rglob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', md.read_text()):
            if target.startswith(('http:', 'https:', 'mailto:', '#')):
                continue
            path = (md.parent / target).resolve()
            if not path.is_relative_to(root) or not path.exists():
                errors.append(f'Broken local Markdown link: {md.name}: {target}')
    skill = root / 'skills/byui-brand-guide/SKILL.md'
    if not skill.read_text().startswith('---\nname: byui-brand-guide\ndescription: '):
        errors.append('Invalid skill header')
    if len(skill.read_text().split()) > 900:
        errors.append('Core skill exceeds 900-word budget; move conditional detail to references')
    for path in root.rglob('*'):
        if '.git' not in path.parts and path.is_symlink() and any(p in path.parts for p in ('assets', 'skills', '.codex-plugin')):
            errors.append(f'Symlink in plugin content: {path}')
    return errors


if __name__ == '__main__':
    issues = validate()
    if issues:
        raise SystemExit('\n'.join(issues))
    print('PASS: manifests, inventory hashes, template integrity/relationships, layout index, local links, and core size')
