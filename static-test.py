"""Static source checks for the Sure HAOS all-in-one package."""
from pathlib import Path
import subprocess
import struct
import yaml

ROOT = Path(__file__).resolve().parent
APP = ROOT / 'sure_all_in_one'
cfg = yaml.safe_load((APP / 'config.yaml').read_text())
repo = yaml.safe_load((ROOT / 'repository.yaml').read_text())
assert repo['name']
assert repo['url'] == 'https://github.com/CookieSource/haos-sure'
assert cfg['slug'] == APP.name
assert cfg['arch'] == ['amd64']
assert cfg['ports'] == {'3443/tcp': 1234}, 'Only the HTTPS frontend should be exposed'
assert cfg['ingress'] is True
assert cfg['ingress_port'] == 8099
assert cfg['panel_title'] == 'Sure'
assert cfg['options']['ssl'] is True
assert any(item.get('type') == 'ssl' for item in cfg['map'])

def png_size(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    return struct.unpack('>II', data[16:24])

assert png_size(APP / 'icon.png') == (128, 128)
assert png_size(APP / 'logo.png') == (256, 256)
assert 'image' not in cfg, 'HA should build locally from the Dockerfile'
assert 'onboarding_state' in cfg['options']
assert 'onboarding_state' in cfg['schema']

dockerfile = (APP / 'Dockerfile').read_text()
assert 'FROM ghcr.io/we-promise/sure:stable' in dockerfile
assert 'postgresql-16' in dockerfile and 'redis-server' in dockerfile
assert 'POSTHOG_FEEDBACK_ENABLED=false' in dockerfile
assert 'EXPOSE 3000 3443 8099' in dockerfile

script_paths = list((APP / 'scripts').glob('*'))
assert len(script_paths) >= 6
for script in script_paths:
    subprocess.run(['bash', '-n', str(script)], check=True)

init = (APP / 'scripts' / 'sure-ha-init').read_text()
assert 'openssl rand -hex 64' in init
assert 'if [[ ! -f /data/private/sure-secrets.env ]]' in init
assert 'unset MCP_API_TOKEN' in init
assert 'auth-host=scram-sha-256' in init
assert 'auth-local=peer' in init
assert 'POSTGRES_PASSWORD' in init
for encryption_key in [
    'ACTIVE_RECORD_ENCRYPTION_PRIMARY_KEY',
    'ACTIVE_RECORD_ENCRYPTION_DETERMINISTIC_KEY',
    'ACTIVE_RECORD_ENCRYPTION_KEY_DERIVATION_SALT',
]:
    assert f'export {encryption_key}' in init
    assert f"printf '{encryption_key}=%s\\n'" in init

supervisor = (APP / 'supervisor' / 'sure.conf').read_text()
for service in ['sure-postgres', 'sure-redis', 'sure-db-init', 'sure-web', 'sure-worker', 'sure-ingress', 'sure-backups']:
    assert f'[program:{service}]' in supervisor
assert 'listen_addresses=127.0.0.1' in supervisor
assert '--bind 127.0.0.1' in supervisor

print('PASS: HAOS metadata, config, service isolation, scripts and image definition')
print('NOTE: this script performs static checks only; run container and HAOS tests separately')
