#!/usr/bin/env python3
"""Check portable asset references and integrity; does not assess visual quality."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', help='Check one model; omitted checks all models')
    parser.add_argument('--root', type=Path, help='Override skill root for portability checks')
    args = parser.parse_args()
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    try:
        catalog = json.loads((root / 'assets/catalog.json').read_text(encoding='utf-8'))
        from PIL import Image
    except (OSError, ValueError, ImportError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False))
        return 1
    model = args.model.upper() if args.model else None
    if model and model not in catalog['models']:
        print(json.dumps({'ok': False, 'error': 'Unknown model', 'supported': list(catalog['models'])}))
        return 1
    selected = {model: catalog['models'][model]} if model else catalog['models']
    images = list(catalog['accessories'].values())
    if not model:
        images += catalog['layout_references'] + catalog['pending_review']
    errors = []

    def inside(relative):
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError('Path escapes skill root: ' + relative)
        return path

    for name, entry in selected.items():
        try:
            inside(entry['identity']).read_text(encoding='utf-8')
        except (OSError, ValueError) as exc:
            errors.append({'model': name, 'error': str(exc)})
        images.extend(entry['images'])
    for entry in images:
        try:
            path = inside(entry['path'])
            if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError('Hash mismatch; review updated image and catalog')
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                im.load()
                if min(im.size) <= 0:
                    raise ValueError('Invalid dimensions')
        except (OSError, ValueError, SyntaxError) as exc:
            errors.append({'path': entry['path'], 'error': str(exc)})
    for key in catalog['bundle']['base'] + catalog['bundle']['optional']:
        if key not in catalog['accessories']:
            errors.append({'error': 'Missing bundle accessory: ' + key})
    print(json.dumps({'ok': not errors, 'models': list(selected), 'images_checked': len(images),
                      'errors': errors, 'scope': 'file integrity only; visual review required'},
                     ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
