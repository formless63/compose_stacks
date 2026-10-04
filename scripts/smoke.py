#!/usr/bin/env python3
"""Exercise a stack using temporary named volumes and loopback-only random ports.

No user .env files, bind-mounted data, fixed container names, or external networks
are used. All test resources are removed on success or failure.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import time
import urllib.request
import uuid

from validate import fixture, resolve

ENDPOINTS = {
    'bitmappery': ('bitmappery', 5173, '/'),
    'super-productivity': ('supersync', 1900, '/health'),
    'penpot': ('penpot-frontend', 8080, '/'),
    'directus': ('directus', 8055, '/server/ping'),
    'portabase': ('portabase', 80, '/api/health'),
    'storyteller': ('storyteller', 8001, '/'),
    'readmeabook': ('readmeabook', 3030, '/api/health'),
}
HTTP = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def run(command, **kwargs):
    result = subprocess.run(command, text=True, capture_output=True, **kwargs)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        result.check_returncode()
    return result.stdout


def smoke(stack, images):
    result = resolve(stack)
    if result.returncode:
        raise RuntimeError(result.stderr)
    model = json.loads(result.stdout)
    project = 'compose-smoke-' + uuid.uuid4().hex[:12]
    model['name'] = project
    model['volumes'] = {}
    # Always create private project networks, even for normally external networks.
    model['networks'] = {key: {} for key in model.get('networks', {})}
    volume_keys = {}
    for name, service in model['services'].items():
        service.pop('container_name', None)
        service['restart'] = 'no'
        service.pop('pull_policy', None)
        if name in images:
            service['image'] = images[name]
        for number, volume in enumerate(service.get('volumes', [])):
            identity = (volume['type'], volume['source'])
            key = volume_keys.setdefault(identity, f'{name}-data-{number}')
            model['volumes'][key] = {}
            volume.update(type='volume', source=key)
            volume.pop('bind', None)
        for port in service.get('ports', []):
            port.update(host_ip='127.0.0.1', published='0')
    if stack == 'directus':
        service = model['services']['directus']
        service['environment'].update(DB_HOST='smoke-db', DB_PORT='5432', DB_DATABASE='directus', DB_USER='directus')
        service['depends_on']['smoke-db'] = {'condition': 'service_healthy'}
        model['services']['smoke-db'] = {
            'image': 'postgres:15-alpine',
            'environment': {'POSTGRES_DB': 'directus', 'POSTGRES_USER': 'directus', 'POSTGRES_PASSWORD': fixture(stack)['DB_PASSWORD']},
            'networks': ['directus'],
            'healthcheck': {'test': ['CMD-SHELL', 'pg_isready -U directus -d directus'], 'interval': '2s', 'timeout': '5s', 'retries': 30},
        }
    if stack == 'penpot':
        # SMTP is an isolated mail sink, never a real external provider.
        model['services']['smoke-mail'] = {'image': 'sj26/mailcatcher:latest', 'networks': ['penpot']}
        model['services']['penpot-backend']['environment'].update(PENPOT_SMTP_HOST='smoke-mail', PENPOT_SMTP_PORT='1025', PENPOT_SMTP_TLS='false', PENPOT_SMTP_SSL='false')
    with tempfile.TemporaryDirectory(prefix=project) as directory:
        path = Path(directory) / 'compose.json'
        path.write_text(json.dumps(model))
        command = ['docker', 'compose', '-p', project, '-f', str(path)]
        try:
            # Compose waits for healthy dependencies and successful migrations.
            run(command + ['up', '-d'], timeout=900)
            service, port, endpoint = ENDPOINTS[stack]
            def url():
                binding = run(command + ['port', service, str(port)]).strip()
                return 'http://' + binding
            def request(endpoint):
                with HTTP.open(url() + endpoint, timeout=10) as response:
                    return response.read(), response.headers
            deadline = time.monotonic() + 240
            while True:
                try:
                    body, headers = request(endpoint)
                    if stack in ('bitmappery', 'penpot', 'storyteller'):
                        assert b'<html' in body.lower(), 'Expected HTML application'
                    elif stack == 'directus':
                        assert body == b'pong', 'Expected Directus server ping'
                    else:
                        data = json.loads(body)
                        assert data, 'Empty health response'
                        if stack == 'super-productivity':
                            assert data['status'] == 'ok' and data['db'] == 'connected', data
                    break
                except Exception:
                    if time.monotonic() >= deadline:
                        raise
                    time.sleep(2)
            if stack == 'bitmappery':
                assert b'bitmappery' in body.lower()
                import re
                asset = re.search(rb'(?:src|href)="((?:\./|/)assets/[^\"]+\.js)"', body)
                assert asset, 'Compiled application script missing'
                assert request('/' + asset[1].decode().lstrip('./'))[0], 'Compiled script empty'
                assert request('/smoke/spa-route')[0] == body, 'SPA fallback failed'
            if stack == 'super-productivity':
                count = run(command + ['exec', '-T', 'db', 'psql', '-U', 'supersync', '-d', 'supersync_db', '-Atc', 'SELECT count(*) FROM _prisma_migrations WHERE finished_at IS NOT NULL'])
                assert int(count.strip()) > 0, 'No successful migrations'
                app_binding = run(command + ['port', 'app', '80']).strip()
                with HTTP.open('http://' + app_binding, timeout=15) as response:
                    assert b'<html' in response.read().lower()
            if stack == 'penpot':
                # A real backend RPC exercises the initialized DB through nginx.
                deadline = time.monotonic() + 240
                while True:
                    try:
                        req = urllib.request.Request(url() + '/api/rpc/command/get-profile', data=b'{}', headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'X-Client': 'compose-smoke'})
                        with HTTP.open(req, timeout=10) as response:
                            assert b'Anonymous User' in response.read()
                        break
                    except Exception:
                        if time.monotonic() >= deadline:
                            raise
                        time.sleep(2)
                # Launch the actual browser bundled with the exporter.
                browser_test = """const {chromium}=require('playwright'); (async()=>{const b=await chromium.launch({args:['--no-sandbox']});try{const p=await b.newPage();await p.setContent('<title>Compose exporter smoke</title><p id=check>works</p>');if(await p.title()!=='Compose exporter smoke'||await p.locator('#check').textContent()!=='works')throw Error('Browser content mismatch');}finally{await b.close();}})().catch(e=>{console.error(e);process.exit(1)});"""
                run(command + ['exec', '-T', 'penpot-exporter', 'node', '-e', browser_test], timeout=120)
            if stack == 'directus':
                # Exercise authentication against the initialized disposable database.
                req = urllib.request.Request(url() + '/auth/login', data=json.dumps({'email': fixture(stack)['DIRECTUS_ADMIN_EMAIL'], 'password': fixture(stack)['DIRECTUS_ADMIN_PASSWORD']}).encode(), headers={'Content-Type': 'application/json'})
                with HTTP.open(req, timeout=15) as response:
                    token = json.load(response)['data']['access_token']
                health = urllib.request.Request(url() + '/server/health', headers={'Authorization': 'Bearer ' + token})
                with HTTP.open(health, timeout=15) as response:
                    assert json.load(response)['status'] == 'ok'
            # Verify app volumes survive a container restart.
            cid = run(command + ['ps', '-q', service]).strip()
            target = model['services'][service].get('volumes', [{}])[0].get('target')
            if target:
                marker = target.rstrip('/') + '/.compose-smoke-persistence'
                run(['docker', 'exec', cid, 'sh', '-c', 'printf compose-smoke > "$1"', 'sh', marker])
                run(command + ['restart', service], timeout=120)
                assert run(['docker', 'exec', cid, 'cat', marker]) == 'compose-smoke'
            details = []
            for name, spec in model['services'].items():
                info = json.loads(run(['docker', 'image', 'inspect', spec['image']]))[0]
                details.append({'service': name, 'image': spec['image'], 'id': info['Id'], 'digests': info.get('RepoDigests', [])})
            print(json.dumps({'stack': stack, 'result': 'passed', 'images': details}, indent=2))
        except Exception:
            logs = subprocess.run(command + ['logs', '--no-color', '--tail', '80'], text=True, capture_output=True)
            print(logs.stdout)
            raise
        finally:
            run(command + ['down', '--volumes', '--remove-orphans', '--timeout', '30'], timeout=120)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stack', choices=ENDPOINTS)
    parser.add_argument('--image', action='append', default=[], metavar='SERVICE=IMAGE', help='Use an existing local image for this service')
    args = parser.parse_args()
    images = dict(item.split('=', 1) for item in args.image)
    smoke(args.stack, images)

if __name__ == '__main__':
    main()
