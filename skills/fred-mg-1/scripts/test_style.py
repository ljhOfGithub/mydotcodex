"""验证本地登记、完整性、工程复制与不覆盖行为；不触碰真实风格基线。"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('style.py')


class StyleCommands(unittest.TestCase):
    def setUp(self):
        # 留存小型验证目录，避免自动批量删除文件。
        self.root = Path(tempfile.mkdtemp(prefix='fred-mg-1-test-'))
        self.library = self.root / 'library'
        project = self.library / '模板工程'
        project.mkdir(parents=True)
        (project / '配置.json').write_text('{"scenes":[]}', encoding='utf-8')
        (project / 'index.html').write_text('<html>测试模板</html>', encoding='utf-8')
        (self.library / '风格.json').write_text(json.dumps(dict(id='fred-mg-1', name='fred mg 1', version='test', project='模板工程')), encoding='utf-8')
        files = [dict(path=str(f.relative_to(self.library)), sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in self.library.rglob('*') if f.is_file()]
        (self.library / '基线文件清单.json').write_text(json.dumps(dict(style_id='fred-mg-1', files=files)), encoding='utf-8')
        self.registry = self.root / 'registry.json'

    def call(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), '--registry', str(self.registry), *map(str, args)], capture_output=True, text=True)

    def register(self):
        result = self.call('register', self.library)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_register_info_and_verify(self):
        self.register()
        self.assertEqual(json.loads(self.call('info').stdout)['name'], 'fred mg 1')
        self.assertEqual(json.loads(self.call('verify').stdout)['status'], 'verified')

    def test_init_copies_exact_files_and_refuses_overwrite(self):
        self.register()
        target = self.root / 'new-project'
        result = self.call('init', target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((target / 'index.html').read_bytes(), (self.library / '模板工程/index.html').read_bytes())
        self.assertEqual(json.loads((target / '风格来源.json').read_text())['style_id'], 'fred-mg-1')
        (target / '用户保留.txt').write_text('保留', encoding='utf-8')
        self.assertNotEqual(self.call('init', target).returncode, 0)
        self.assertEqual((target / '用户保留.txt').read_text(), '保留')

    def test_tampered_baseline_is_rejected_before_copy(self):
        self.register()
        (self.library / '模板工程/配置.json').write_text('changed', encoding='utf-8')
        self.assertNotEqual(self.call('verify').returncode, 0)
        target = self.root / 'new-project'
        self.assertNotEqual(self.call('init', target).returncode, 0)
        self.assertFalse(target.exists())

    def test_manifest_cannot_escape_library(self):
        self.register()
        path = self.library / '基线文件清单.json'
        manifest = json.loads(path.read_text())
        manifest['files'].append(dict(path='../outside.txt', sha256='irrelevant'))
        path.write_text(json.dumps(manifest), encoding='utf-8')
        self.assertNotEqual(self.call('verify').returncode, 0)

    def test_unregistered_lookup_and_in_library_copy_are_rejected(self):
        self.assertNotEqual(self.call('info').returncode, 0)
        self.register()
        self.assertNotEqual(self.call('init', self.library / 'recursive').returncode, 0)


if __name__ == '__main__':
    unittest.main()
