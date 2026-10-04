#!/usr/bin/env python3
"""Resolve every active stack with disposable fixtures; never start services."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
STACKS = {
    'qbittorrent-gluetun': ('compose.yaml', '.env.example'),
    'omada': ('compose.yaml', '.env.example'),
    'bitmappery': ('compose.yaml', '.env.example'),
    'super-productivity': ('compose.yaml', '.env.example'),
    'penpot': ('compose.yaml', '.env.example'),
    'directus': ('external-db-compose.yaml', 'external-db-.env.example'),
    'portabase': ('compose.yml', '.env.example'),
    'portabase-agent': ('compose.yml', '.env.example'),
    'storyteller': ('compose.yaml', '.env.example'),
    'readmeabook': ('compose.yaml', '.env.example'),
}
# Public, disposable test values; never deployment credentials.
FIXTURES = {
    'PROTON_KEY': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
    'GLUETUN_PASS': 'ComposeTestOnly123',
    'QBIT_PASS': 'ComposeTestOnly123',
    'POSTGRES_PASSWORD': 'ComposeTestOnly_123',
    'PENPOT_DATABASE_PASSWORD': 'ComposeTestOnly_123',
    'PENPOT_SECRET_KEY': 'a' * 86,
    'JWT_SECRET': 'b' * 64,
    'PROJECT_SECRET': 'c' * 64,
    'DIRECTUS_SECRET': 'd' * 64,
    'DIRECTUS_ADMIN_PASSWORD': 'ComposeTestOnly_123!',
    'DB_PASSWORD': 'ComposeTestOnly_123',
    'EDGE_KEY': 'ComposeValidationOnly',
    'STORYTELLER_SECRET_KEY': 'e' * 64,
}

def fixture(stack):
    compose, example = STACKS[stack]
    text = (ROOT / stack / example).read_text()
    values = {}
    for line in text.splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            values[key] = value
    for key in values.keys() & FIXTURES.keys():
        values[key] = FIXTURES[key]
    return values


def resolve(stack, values=None, extra=()):
    compose, _ = STACKS[stack]
    source = ROOT / stack / compose
    variables = set(re.findall(r'\$\{([A-Z][A-Z0-9_]*)', source.read_text()))
    env = {k: v for k, v in os.environ.items() if k not in variables}
    with tempfile.TemporaryDirectory(prefix='compose-config-') as temp:
        envfile = Path(temp) / 'fixture.env'
        envfile.write_text(''.join(f'{k}={v}\n' for k, v in (values if values is not None else fixture(stack)).items()))
        command = ['docker', 'compose', '--env-file', str(envfile), '-f', str(source)]
        for path in extra:
            command += ['-f', str(ROOT / stack / path)]
        return subprocess.run(command + ['config', '--format', 'json'], env=env, text=True, capture_output=True)


def main():
    # Every active template must be registered, so new folders cannot silently
    # escape validation. Overlay files are validated with their base stack.
    registered = {ROOT / stack / files[0] for stack, files in STACKS.items()}
    registered.add(ROOT / 'portabase' / 'compose.proxy.yml')
    found = {p for p in ROOT.glob('*/*compose.y*ml') if not p.parts[-2].startswith('.')}
    missing = found - registered
    assert not missing, f'Register new compose templates in STACKS: {sorted(str(p.relative_to(ROOT)) for p in missing)}'
    count = negative = 0
    for stack, (compose, example) in STACKS.items():
        result = resolve(stack)
        if result.returncode:
            raise RuntimeError(f'{stack}: {result.stderr}')
        assert not result.stderr.strip(), f'{stack}: interpolation warning: {result.stderr}'
        model = json.loads(result.stdout)
        assert model['services'], stack
        source = (ROOT / stack / compose).read_text()
        declared = fixture(stack)
        bare = set(re.findall(r'\$\{([A-Z][A-Z0-9_]*)\}', source))
        assert bare <= declared.keys(), f'{stack}: missing example variables {bare - declared.keys()}'
        for required in set(re.findall(r'\$\{([A-Z][A-Z0-9_]*):\?', source)):
            bad = declared.copy()
            bad[required] = ''
            failure = resolve(stack, bad)
            assert failure.returncode != 0 and required in failure.stderr, f'{stack}: missing {required} was accepted'
            negative += 1
        # Image choices belong to .env, so a Git update cannot silently replace
        # an explicitly selected application or database version.
        expressions = re.findall(r'^\s+image:\s*(.+)$', source, flags=re.M)
        assert expressions and all('${' in expression for expression in expressions), f'{stack}: image selection must come from .env'
        image_variables = {key for expression in expressions for key in re.findall(r'\$\{([A-Z][A-Z0-9_]*)', expression)}
        assert image_variables <= declared.keys(), f'{stack}: missing image settings in example'
        selected = declared.copy()
        for key in image_variables:
            selected[key] = 'example.com/env-selection:keep-this-version' if key.endswith('_IMAGE') else 'keep-this-version'
        changed = resolve(stack, selected)
        assert changed.returncode == 0, changed.stderr
        choices = json.loads(changed.stdout)['services']
        assert all('keep-this-version' in item['image'] for item in choices.values()), f'{stack}: an image ignored .env'
        if stack == 'qbittorrent-gluetun':
            services = model['services']
            assert services['qbittorrent']['network_mode'] == 'service:gluetun'
            vpn = services['gluetun']
            assert vpn['environment']['FIREWALL_OUTBOUND_SUBNETS'] == ''
            assert vpn['environment']['FIREWALL_INPUT_PORTS'] == '8080,8000'
            assert 'VPN_PORT_FORWARDING_UP_COMMAND' not in vpn['environment']
            assert [port['target'] for port in vpn['ports']] == [8080]
            for ui in ('gluetun-webui', 'qbit_manage'):
                assert services[ui]['ports'][0]['host_ip'] == '127.0.0.1'
            # Catch JSON-breaking control credentials before deployment.
            auth = json.loads(vpn['environment']['HTTP_CONTROL_SERVER_AUTH_DEFAULT_ROLE'])
            assert auth['password'] == declared['GLUETUN_PASS']
            assert all(not service.get('labels') for service in services.values())
        if stack == 'portabase':
            proxy = resolve(stack, extra=('compose.proxy.yml',))
            assert proxy.returncode == 0, proxy.stderr
            assert 'newt_net' in json.loads(proxy.stdout)['services']['portabase']['networks']
        if stack == 'super-productivity':
            assert model['services']['supersync']['depends_on']['migrate']['condition'] == 'service_completed_successfully'
            assert model['services']['supersync']['image'] == model['services']['migrate']['image']
        if stack == 'portabase-agent':
            env = model['services']['portabase-agent']['environment']
            assert env['POOLING'] == declared['POLLING'] and 'POLLING' not in env
            json.loads((ROOT / stack / 'databases.example.json').read_text())
        if stack == 'storyteller':
            assert model['services']['storyteller']['environment']['AUTH_URL'] == declared['AUTH_URL']
        print(f'PASS {stack}')
        count += 1
    print(f'{count} stacks resolved; {negative} missing-required-variable checks passed; proxy overlay passed.')

if __name__ == '__main__':
    main()
