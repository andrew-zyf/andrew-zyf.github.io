"""Build every follower portrait from a verified public DOM snapshot."""
import argparse, base64, json, math, re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from PIL import Image, ImageOps

parser = argparse.ArgumentParser()
parser.add_argument('snapshot', type=Path)
parser.add_argument('cache', type=Path)
args = parser.parse_args()
workspace = Path('/Users/az/Projects/codex').resolve()
output = Path(__file__).resolve().parents[1] / 'public'
for path in (args.cache, output):
    assert path.resolve().is_relative_to(workspace)
    path.mkdir(parents=True, exist_ok=True)
people = json.loads(args.snapshot.read_text())
assert len({p['handle'].lower() for p in people}) == len(people)
people.sort(key=lambda p: p['handle'].lower())

def download(person):
    handle = person['handle']
    assert re.fullmatch(r'[A-Za-z0-9_]{1,15}', handle)
    path = args.cache / (handle + '.png')
    source = person['avatarSourceUrl']
    if path.exists():
        return {'handle': handle, 'status': 'ok', 'path': str(path)}
    candidates = [source]
    if source.startswith('https://pbs.twimg.com/profile_images/'):
        high = re.sub(r'_(normal|bigger|x96)(\.[A-Za-z]+)$', r'_400x400\2', source)
        candidates = list(dict.fromkeys([high, source]))
    error = ''
    for url in candidates:
        try:
            if url.startswith('data:image/'):
                raw = base64.b64decode(url.split(',', 1)[1])
            else:
                with urlopen(url, timeout=20) as response:
                    raw = response.read()
            with Image.open(BytesIO(raw)) as image:
                ImageOps.exif_transpose(image).convert('RGB').save(path)
            return {'handle': handle, 'status': 'ok', 'path': str(path)}
        except Exception as exc:
            error = str(exc)
    return {'handle': handle, 'status': 'error', 'error': error}

with ThreadPoolExecutor(max_workers=12) as executor:
    downloads = []
    for result in executor.map(download, people):
        downloads.append(result)
        if len(downloads) % 100 == 0:
            print(f'Downloaded {len(downloads)}/{len(people)}', flush=True)
(args.cache / 'downloads.json').write_text(json.dumps(downloads, ensure_ascii=False, indent=2))
failed = [d for d in downloads if d['status'] != 'ok']
assert not failed, f'{len(failed)} avatars failed; inspect downloads.json and retry before publishing.'
columns, size = 40, 96
rows = math.ceil(len(people) / columns)
atlas = Image.new('RGB', (columns * size, rows * size), '#161616')
for index, result in enumerate(downloads):
    with Image.open(result['path']) as im:
        tile = ImageOps.fit(im, (size, size), method=Image.Resampling.LANCZOS)
        atlas.paste(tile, (index % columns * size, index // columns * size))
atlas.save(output / 'portraits.webp', 'WEBP', quality=91, method=6)
capacity = max(10, math.ceil((len(people) + 40) / 80) * 2) * 40 - 40
data = {
    'capturedAt': '2026-09-14T11:35:00Z',
    'generatedAt': datetime.now(timezone.utc).isoformat(),
    'source': 'https://x.com/andrew_zyf/followers',
    'selection': 'All 1326 followers read from the current public follower list, including default avatars. Alphabetical layout; not historical follow order.',
    'profileFollowerCount': 1326,
    'layoutCapacity': capacity, 'omittedSlots': capacity - len(people),
    'count': len(people), 'atlasColumns': columns, 'atlasRows': rows,
    'people': [{k: p[k] for k in ('handle', 'displayName', 'profileUrl', 'bio', 'bioStatus', 'bioTranslated')} for p in people],
}
(output / 'people.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
print(json.dumps({'count': len(people), 'dimensions': atlas.size, 'bytes': (output / 'portraits.webp').stat().st_size}))
