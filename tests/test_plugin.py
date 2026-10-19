import hashlib
import importlib.util
import io
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_plugin import check_schema, contained, validate

spec = importlib.util.spec_from_file_location('prepare_pptx', ROOT / 'skills/byui-brand-guide/scripts/prepare_pptx.py')
prepare_pptx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare_pptx)


class PluginReleaseTests(unittest.TestCase):
    def test_package_source_contract(self):
        self.assertEqual(validate(), [])

    def test_declared_schema_rejects_old_root_icon_metadata(self):
        manifest = json.loads((ROOT / 'plugin.json').read_text())
        schema = json.loads((ROOT / 'scripts/schemas/agent-plugins-1.0.0.json').read_text())
        manifest['logo'] = './assets/byui-brand-guide.svg'
        self.assertTrue(any('disallowed property logo' in error for error in check_schema(manifest, schema)))

    def test_paths_cannot_escape_plugin(self):
        with self.assertRaises(ValueError):
            contained(ROOT, '../outside-plugin.png')

    def test_anniversary_copy_requires_prior_confirmation(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'test.pptx'
            with self.assertRaises(ValueError):
                prepare_pptx.prepare('blue', target)
            self.assertFalse(target.exists())

    def test_anniversary_working_copies_preserve_all_native_parts(self):
        # Explicit flag is a test-fixture decision, not production campaign approval.
        for variant in ['blue', 'white']:
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'fixture.pptx'
                prepare_pptx.prepare(variant, output, anniversary_approved=True)
                source = ROOT / f'assets/templates/powerpoint/BYUI_{variant.title()}_Template.potx'
                with ZipFile(source) as original, ZipFile(output) as result:
                    self.assertEqual(original.namelist(), result.namelist())
                    charts = [n for n in original.namelist() if re.fullmatch(r'ppt/charts/chart\d+\.xml', n)]
                    self.assertEqual(len(charts), 7)
                    for name in original.namelist():
                        if name == '[Content_Types].xml':
                            self.assertIn(prepare_pptx.PRESENTATION_TYPE, result.read(name))
                            self.assertNotIn(prepare_pptx.TEMPLATE_TYPE, result.read(name))
                        else:
                            self.assertEqual(original.read(name), result.read(name), name)
                with self.assertRaises(FileExistsError):
                    prepare_pptx.prepare(variant, output, anniversary_approved=True)

    def test_original_pngs_insert_into_docx(self):
        try:
            from docx import Document
            from docx.shared import Inches
        except ImportError:
            self.skipTest('Optional Office smoke check requires python-docx in the artifact runtime')
        document = Document()
        paths = sorted((ROOT / 'assets/logos').glob('*.png'))
        self.assertEqual(len(paths), 4)
        for path in paths:
            document.add_picture(str(path), width=Inches(1.5))
        buffer = io.BytesIO()
        document.save(buffer)
        with ZipFile(buffer) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(len([n for n in archive.namelist() if n.startswith('word/media/')]), 4)

    def test_archive_matches_source_and_excludes_build_noise(self):
        script = ROOT / 'scripts/package_plugin.py'
        def build():
            subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True, stdout=subprocess.PIPE)
            return (ROOT / 'dist/byui-brand-guide-plugin.zip').read_bytes()
        first = build()
        self.assertEqual(hashlib.sha256(first).digest(), hashlib.sha256(build()).digest())
        with ZipFile(io.BytesIO(first)) as archive:
            self.assertIsNone(archive.testzip())
            for name in archive.namelist():
                self.assertTrue(name.startswith('byui-brand-guide/'))
                self.assertNotIn('__pycache__', name)
                self.assertFalse(name.endswith('.pyc'))
                path = ROOT / Path(name).relative_to('byui-brand-guide')
                self.assertEqual(archive.read(name), path.read_bytes())
            self.assertIn('byui-brand-guide/assets/catalog.json', archive.namelist())
            self.assertIn('byui-brand-guide/skills/byui-brand-guide/scripts/prepare_pptx.py', archive.namelist())


if __name__ == '__main__':
    unittest.main()
