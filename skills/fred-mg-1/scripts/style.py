#!/usr/bin/env python3
"""登记、校验并复制本机个人MG风格；不上传媒体，不覆盖现有工程。"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

STYLE_ID = 'fred-mg-1'
DEFAULT_REGISTRY = Path.home() / '.codex/local-assets' / STYLE_ID / 'registry.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    with path.open('rb') as stream:
        h = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def within(root, relative):
    part = Path(relative)
    result = (root / part).resolve()
    if part.is_absolute() or not result.is_relative_to(root.resolve()):
        raise ValueError('风格清单中含目录外路径')
    return result


def inspect_library(root):
    root = root.expanduser().resolve()
    meta = read(root / '风格.json')
    if meta.get('id') != STYLE_ID:
        raise ValueError('这不是 fred mg 1 风格目录')
    project = within(root, meta['project'])
    if not (project / '配置.json').is_file() or not (project / 'index.html').is_file():
        raise ValueError('缺少模板工程的配置或HTML，请恢复完整个人风格包')
    return root, project, meta


def verify(root):
    root, project, meta = inspect_library(root)
    manifest = read(root / '基线文件清单.json')
    if manifest.get('style_id') != STYLE_ID:
        raise ValueError('风格清单身份不符')
    paths = set()
    for entry in manifest['files']:
        rel = entry['path']
        if rel in paths:
            raise ValueError('风格清单包含重复文件')
        paths.add(rel)
        f = within(root, rel)
        if not f.is_file() or digest(f) != entry['sha256']:
            raise ValueError('固定基线文件缺失或变化：' + rel)
    for required in [meta['project'] + '/配置.json', meta['project'] + '/index.html', '风格.json']:
        if required not in paths:
            raise ValueError('风格清单缺少必要文件：' + required)
    return root, project, meta, manifest


def registered(registry):
    if not registry.is_file():
        raise ValueError('本机未登记 fred mg 1；将个人风格包放回本机，再运行 register /风格根目录')
    record = read(registry)
    if record.get('style_id') != STYLE_ID:
        raise ValueError('本机登记身份不符')
    return Path(record['library'])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--registry', type=Path, default=DEFAULT_REGISTRY, help='本机登记文件；通常不需要修改')
    commands = ap.add_subparsers(dest='command', required=True)
    register = commands.add_parser('register', help='登记现有本机风格包')
    register.add_argument('library', type=Path)
    commands.add_parser('info', help='查看当前模板和演示位置')
    commands.add_parser('verify', help='校验固定基线的全部登记文件')
    init = commands.add_parser('init', help='把模板复制为新工程；拒绝覆盖已有目录')
    init.add_argument('output', type=Path)
    args = ap.parse_args()
    registry = args.registry.expanduser().resolve()
    if args.command == 'register':
        root, project, meta, manifest = verify(args.library)
        if registry.exists() and Path(read(registry)['library']).resolve() != root:
            raise ValueError('已有其他风格基线登记；请先核对旧登记，不自动替换')
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(json.dumps(dict(style_id=STYLE_ID, name=meta['name'], version=meta['version'], library=str(root)), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        result = dict(status='registered', name=meta['name'], library=str(root), files=len(manifest['files']))
    else:
        root = registered(registry)
        if args.command == 'info':
            root, project, meta = inspect_library(root)
            result = dict(name=meta['name'], id=STYLE_ID, version=meta['version'], library=str(root), project=str(project), preview=str(within(root, meta['preview'])) if meta.get('preview') else None, comparison=str(within(root, meta['comparison'])) if meta.get('comparison') else None)
        else:
            root, project, meta, manifest = verify(root)
            if args.command == 'verify':
                result = dict(status='verified', name=meta['name'], version=meta['version'], files=len(manifest['files']))
            else:
                output = args.output.expanduser().resolve()
                if output.exists() or output.is_relative_to(root):
                    raise ValueError('目标必须是风格库外不存在的新目录，不覆盖已有工程')
                selected = [entry for entry in manifest['files'] if Path(entry['path']).is_relative_to(meta['project'])]
                output.mkdir(parents=True)
                for entry in selected:
                    relative = Path(entry['path']).relative_to(meta['project'])
                    dest = within(output, str(relative))
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(within(root, entry['path']), dest)
                origin = dict(style_id=STYLE_ID, name=meta['name'], version=meta['version'], baseline_manifest_sha256=digest(root / '基线文件清单.json'), note='这是可编辑副本；新主题需替换示例文案、数据、音轨与字幕。')
                (output / '风格来源.json').write_text(json.dumps(origin, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                result = dict(status='created', project=str(output), files=len(selected), source_style=STYLE_ID)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
