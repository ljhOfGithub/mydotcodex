#!/usr/bin/env python3
"""初始化视频资料包，按固定提交续取 GitHub 原文，不执行仓库代码。"""
import argparse
import base64
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit


def repository(value):
    value = value.strip().rstrip('/')
    if '://' in value:
        url = urlsplit(value)
        if url.scheme != 'https' or url.netloc.lower() != 'github.com' or url.query or url.fragment:
            raise ValueError('只接受不含凭据和查询参数的 GitHub HTTPS 仓库根链接')
        value = url.path.strip('/')
    if value.endswith('.git'):
        value = value[:-4]
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+', value):
        raise ValueError('请提供 OWNER/REPO 或仓库根链接，不使用分支或文件链接')
    if value.split('/')[1] in ('.', '..'):
        raise ValueError('仓库名称无效')
    return value


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def initialize(url, output, audience='', seconds=60):
    repo = repository(url)
    if seconds <= 0:
        raise ValueError('目标秒数须大于零')
    root = Path(output).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=False)
    for folder in ('sources', 'assets', 'edit', 'production', 'evidence', 'outputs'):
        (root / folder).mkdir()
    save(root / 'project.json', {
        'format': 'github2video.project@1', 'repository': repo,
        'url': 'https://github.com/' + repo, 'language': 'zh-CN',
        'requested_compositor': 'hypit', 'creation_mode': 'original',
        'audience': audience, 'target_seconds': seconds,
        'canvas': {'width': 1920, 'height': 1080, 'fps': 30},
        'narration': {'state': 'pending', 'approved_audio': None}, 'reference_video': None,
    })
    save(root / 'edit/facts.json', {'facts': []})
    save(root / 'edit/storyboard.json', {'timing': 'unplanned', 'shots': []})
    save(root / 'evidence/state.json', {
        'stage': 'initialized', 'build_id': None, 'pid': None,
        'approvals': [], 'checks': {}, 'artifacts': [],
    })
    return root


def gh_api(endpoint):
    response = subprocess.run(['gh', 'api', endpoint], capture_output=True, text=True, timeout=45)
    if response.returncode:
        if 'HTTP 404' in response.stderr:
            return None
        raise RuntimeError(f'GitHub 读取失败（退出 {response.returncode}）：{endpoint}')
    return json.loads(response.stdout)


def source_path(value):
    if (not value or value.startswith('/') or '\\' in value
            or any(x in ('', '.', '..') for x in value.split('/'))):
        raise ValueError('源码路径必须是仓库内的明确文件，不能含路径跳转')
    return value


def collect(root, files=(), api=gh_api):
    root = Path(root).expanduser().resolve()
    project = json.loads((root / 'project.json').read_text(encoding='utf-8'))
    repo = repository(project['repository'])
    files = [source_path(f) for f in files]
    lock_path = root / 'sources/source-lock.json'
    if lock_path.exists():
        lock = json.loads(lock_path.read_text(encoding='utf-8'))
        if lock['repository'] != repo:
            raise ValueError('项目仓库与已冻结资料不同，请另建项目')
    else:
        meta = api('repos/' + repo)
        if meta is None:
            raise ValueError('仓库不存在或当前账号无法访问')
        commit = api(f"repos/{repo}/commits/{quote(meta['default_branch'], safe='')}")
        if commit is None or not re.fullmatch('[a-f0-9]{40}', commit['sha']):
            raise ValueError('无法冻结有效提交')
        lock = {'repository': repo, 'commit': commit['sha'],
                'retrieved_at': datetime.now(timezone.utc).isoformat(),
                'default_branch': meta['default_branch'], 'license': meta.get('license'),
                'fork': meta.get('fork'), 'parent': (meta.get('parent') or {}).get('full_name'),
                'files': {}}
        save(lock_path, lock)
    commit = lock['commit']
    requests = [('README', f'repos/{repo}/readme?ref={commit}'),
                ('LICENSE', f'repos/{repo}/license?ref={commit}')]
    requests += [(f, f'repos/{repo}/contents/{quote(f, safe="/")}?ref={commit}') for f in files]
    state_path = root / 'evidence/state.json'
    state = json.loads(state_path.read_text(encoding='utf-8'))
    if state.get('stage') in ('initialized', 'collecting', 'collection_failed'):
        state['stage'] = 'collecting'
    save(state_path, state)
    try:
        for key, endpoint in requests:
            if key in lock['files']:
                entry = lock['files'][key]
                if entry['status'] == 'missing':
                    continue
                target = root / entry['path']
                if not target.is_file() or sha(target) != entry['sha256']:
                    raise ValueError(f'已冻结资料被改动或缺失：{key}')
                continue
            data = api(endpoint)
            if data is None:
                lock['files'][key] = {'status': 'missing', 'endpoint': endpoint}
                save(lock_path, lock)
                continue
            if data.get('encoding') != 'base64' or data.get('size', 0) > 3_000_000:
                raise ValueError(f'资料不是可直接保存的小型原始文件：{key}')
            rel = source_path(data['path'])
            target = root / 'sources/raw' / rel
            if target.exists():
                raise FileExistsError(f'拒绝覆盖未登记文件：{target}')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(base64.b64decode(data['content']))
            lock['files'][key] = {'status': 'saved', 'path': target.relative_to(root).as_posix(),
                                  'sha256': sha(target), 'endpoint': endpoint,
                                  'url': f'https://github.com/{repo}/blob/{commit}/{quote(rel, safe="/")}'}
            save(lock_path, lock)
        if state.get('stage') == 'collecting':
            state['stage'] = 'sources_collected'
        state.pop('collection_error', None)
    except Exception as exc:
        if state.get('stage') == 'collecting':
            state['stage'] = 'collection_failed'
        state['collection_error'] = str(exc)
        raise
    finally:
        save(state_path, state)
    return lock


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init', help='建立资料包，不覆盖已有目录')
    init.add_argument('url')
    init.add_argument('--output', required=True)
    init.add_argument('--audience', default='')
    init.add_argument('--seconds', type=int, default=60)
    init.add_argument('--fetch', action='store_true')
    resume = commands.add_parser('collect', help='按冻结提交续取资料')
    resume.add_argument('project')
    resume.add_argument('--file', action='append', default=[])
    args = parser.parse_args()
    try:
        if args.command == 'init':
            root = initialize(args.url, args.output, args.audience, args.seconds)
            if args.fetch:
                collect(root)
        else:
            root = Path(args.project).expanduser().resolve()
            collect(root, args.file)
        print(json.dumps({'project': str(root), 'state': str(root / 'evidence/state.json')}, ensure_ascii=False))
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f'未完成：{exc}\n现有资料保持原位，请检查状态后使用 collect 继续。\n')


if __name__ == '__main__':
    main()
