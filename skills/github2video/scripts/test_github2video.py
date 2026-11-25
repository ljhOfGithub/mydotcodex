"""验证固定提交、资料不覆盖和中断续取；不运行真实项目或调用网络。"""
import base64
import json
import tempfile
import unittest
from pathlib import Path
from github2video import collect, initialize, repository, source_path


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix='github2video-test-')) / 'project'
        self.calls = []
        self.commit = 'a' * 40

    def api(self, endpoint):
        self.calls.append(endpoint)
        if endpoint == 'repos/owner/repo':
            return {'default_branch': 'main', 'license': None, 'fork': False}
        if '/commits/' in endpoint:
            return {'sha': self.commit}
        if '/license?' in endpoint:
            return None
        rel = 'README.md' if '/readme?' in endpoint else 'src/demo.py'
        return {'path': rel, 'size': 8, 'encoding': 'base64',
                'content': base64.b64encode(b'example\n').decode()}

    def test_repository_root_only(self):
        self.assertEqual(repository('https://github.com/owner/repo.git/'), 'owner/repo')
        for url in ('https://github.com/owner/repo/blob/main/a', 'https://github.com.evil/owner/repo',
                    'https://user@github.com/owner/repo', 'https://github.com:443/owner/repo',
                    'https://github.com/owner/repo?x=1', 'owner/..', 'file:///owner/repo'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                repository(url)

    def test_existing_project_not_overwritten(self):
        initialize('owner/repo', self.root)
        record = self.root / 'project.json'
        before = record.read_bytes()
        with self.assertRaises(FileExistsError):
            initialize('other/repo', self.root)
        self.assertEqual(record.read_bytes(), before)

    def test_commit_is_pinned_and_missing_license_not_invented(self):
        initialize('owner/repo', self.root)
        lock = collect(self.root, ['src/demo.py'], self.api)
        self.assertEqual(lock['commit'], 'a' * 40)
        self.assertEqual(lock['files']['LICENSE']['status'], 'missing')
        self.assertIsNone(lock['license'])
        self.assertTrue(all('ref=' + 'a' * 40 in x for x in self.calls if '/readme?' in x or '/contents/' in x))
        self.commit = 'b' * 40
        self.calls.clear()
        self.assertEqual(collect(self.root, ['src/demo.py'], self.api)['commit'], 'a' * 40)
        self.assertEqual(self.calls, [])

    def test_changed_snapshot_detected(self):
        initialize('owner/repo', self.root)
        collect(self.root, api=self.api)
        (self.root / 'sources/raw/README.md').write_text('changed')
        with self.assertRaisesRegex(ValueError, '已冻结资料'):
            collect(self.root, api=self.api)

    def test_network_failure_resumes_original_commit(self):
        initialize('owner/repo', self.root)
        def fails(endpoint):
            if '/readme?' in endpoint:
                raise RuntimeError('网络中断')
            return self.api(endpoint)
        with self.assertRaises(RuntimeError):
            collect(self.root, api=fails)
        state_path = self.root / 'evidence/state.json'
        self.assertEqual(json.loads(state_path.read_text())['stage'], 'collection_failed')
        self.commit = 'b' * 40
        lock = collect(self.root, api=self.api)
        self.assertEqual(lock['commit'], 'a' * 40)
        self.assertEqual(json.loads(state_path.read_text())['stage'], 'sources_collected')

    def test_collection_preserves_later_stage(self):
        initialize('owner/repo', self.root)
        state_path = self.root / 'evidence/state.json'
        state = json.loads(state_path.read_text())
        state.update(stage='approved_frozen', build_id='existing-build', approvals=['existing'])
        state_path.write_text(json.dumps(state))
        collect(self.root, api=self.api)
        self.assertEqual(json.loads(state_path.read_text()), state)

    def test_source_path_cannot_escape(self):
        for path in ('../config', '/etc/passwd', 'src/../../config', 'a\\b', 'a//b'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                source_path(path)


if __name__ == '__main__':
    unittest.main()
