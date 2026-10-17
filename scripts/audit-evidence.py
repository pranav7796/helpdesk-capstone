"""Validate the final capstone evidence inventory without touching private files."""
from pathlib import Path
import datetime
import hashlib
import json
import struct
import subprocess
import zlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence/final-2026-10-17'

def read(name):
    return json.loads((OUT / name).read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def png(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', str(path)
    offset, chunks, ended, size = 8, [], False, None
    while offset < len(data):
        length = struct.unpack('>I', data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        crc = struct.unpack('>I', data[offset + 8 + length:offset + 12 + length])[0]
        assert zlib.crc32(kind + payload) & 0xffffffff == crc, str(path)
        if kind == b'IHDR':
            size = struct.unpack('>II', payload[:8])
        if kind == b'IDAT':
            chunks.append(payload)
        if kind == b'IEND':
            ended = True
        offset += length + 12
    assert ended and size and zlib.decompress(b''.join(chunks)), str(path)
    return {'width': size[0], 'height': size[1]}

if __name__ == '__main__':
    criteria = read('criterion-evidence.json')
    assert len(criteria) == 46 and sum(c['points'] for c in criteria) == 100
    verified = [c for c in criteria if c['status'] == 'VERIFIED']
    for row in criteria:
        for filename in row['screenshots']:
            path = ROOT / filename
            assert path.is_file() and path.resolve().is_relative_to(ROOT / 'evidence/screenshots'), filename
    prior = json.loads((ROOT / 'evidence/sydney/inventory.json').read_text())
    old_reviews = {x['path']: x for x in prior['files'] if x['path'].endswith('.png')}
    records = []
    for record in read('archive-screenshot-map.json'):
        assert digest(ROOT / record['source']) == record['sha256'] == digest(ROOT / record['screenshot'])
        assert old_reviews[record['source']]['sha256'] == record['sha256']
        record['visual_review'] = old_reviews[record['source']]['visual_review']
        records.append(record)
    fresh = read('terminal-capture-manifest.json') + read('public-capture-manifest.json') + read('browser-capture-manifest.json')
    fresh += read('monitoring-correction-capture.json')['screenshots']
    reviews = read('screenshot-reviews.json')
    for record in fresh:
        assert record.get('exit_code', 0) == 0
        assert record.get('http_status') in (None, 200)
        assert digest(ROOT / record['screenshot']) == record['sha256']
        record['visual_review'] = reviews[record['screenshot']]
        records.append(record)
    by_file = {r['screenshot']: r for r in records}
    actual_files = {str(p.relative_to(ROOT)) for p in (ROOT / 'evidence/screenshots').glob('*.png')}
    assert actual_files == set(by_file), 'A screenshot lacks provenance or visual review'
    for record in by_file.values():
        record.update(png(ROOT / record['screenshot']))
    videos = read('archive-video-map.json') + [read('platform-video-manifest.json'), read('monitoring-correction-capture.json')]
    for record in videos:
        path = ROOT / record['path']
        assert digest(path) == record['sha256']
        record['probe'] = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_name,width,height', '-of', 'json', str(path)], text=True))
    # Parse every public evidence JSON; exclude private credentials and this report.
    for path in (ROOT / 'evidence').rglob('*.json'):
        if 'private' not in path.relative_to(ROOT / 'evidence').parts and path.name != 'evidence-audit.json':
            json.loads(path.read_text())
    report = {'audited_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'criteria_total': 46, 'verified_criteria': len(verified),
              'estimated_verified_points': sum(c['points'] for c in verified),
              'unverified_criteria': [c['id'] + ': ' + c['criterion'] for c in criteria if c['status'] != 'VERIFIED'],
              'screenshot_count': len(by_file), 'fresh_screenshot_count': len(fresh),
              'archived_screenshot_count': len(by_file) - len(fresh), 'video_count': len(videos),
              'errors': [], 'screenshots': list(by_file.values()), 'videos': videos,
              'scope': 'All public JSON, every canonical screenshot, criterion screenshot references, and canonical video hashes/probes. Private files excluded. Authenticity/readability rely on observed capture provenance and recorded visual review; checksums alone do not prove authenticity.'}
    (OUT / 'evidence-audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('screenshots', 'videos')}, indent=2))
