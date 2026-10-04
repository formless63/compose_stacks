#!/usr/bin/env python3
"""Test dashboard setup in disposable containers; simulate the control API, never start a VPN.
Pull the two dashboard images before running. Does not read deployment .env.
"""
import json, subprocess, tempfile, time, urllib.request
from pathlib import Path

def docker(*args):
    return subprocess.check_output(['docker',*args],text=True).strip()
def get(port,path):
    with urllib.request.urlopen(f'http://127.0.0.1:{port}{path}',timeout=8) as response:
        return response.read()
ROOT = Path(__file__).resolve().parents[2]
network='vpn-review-dashboards'
names=['vpn-review-control','vpn-review-ui','vpn-review-manage']
with tempfile.TemporaryDirectory(prefix='vpn-dashboard-') as d:
    path=Path(d)
    (path/'config').mkdir(); (path/'downloads').mkdir()
    (path/'config/config.yml').write_text((ROOT / 'qbittorrent-gluetun/qbit-manage.example.yml').read_text())
    # A fake authenticated control API tests the dashboard wiring, not a VPN.
    (path/'control.js').write_text("const http=require('http'); http.createServer((q,r)=>{if(q.headers.authorization!=='Basic '+Buffer.from('test:TestOnly123').toString('base64')){r.writeHead(401);r.end();return;}r.setHeader('Content-Type','application/json');r.end(JSON.stringify({status:'running', public_ip:'203.0.113.1',port:12345}));}).listen(8000,'0.0.0.0');")
    try:
        docker('network','create',network)
        docker('run','-d','--name',names[0],'--network',network,'--network-alias','gluetun','-v',f'{path}/control.js:/control.js:ro','node:24-alpine','node','/control.js')
        docker('run','-d','--name',names[1],'--network',network,'-p','127.0.0.1::3000','--read-only','--tmpfs','/tmp','--cap-drop','ALL','--security-opt','no-new-privileges:true','-e','GLUETUN_CONTROL_URL=http://gluetun:8000','-e','GLUETUN_USER=test','-e','GLUETUN_PASSWORD=TestOnly123','scuzza/gluetun-webui:latest')
        docker('run','-d','--name',names[2],'--network',network,'-p','127.0.0.1::8181','-e','PUID=1000','-e','PGID=1000','-e','QBT_WEB_SERVER=true','-e','QBT_RUN=false','-e','QBT_STARTUP_DELAY=86400','-e','QBIT_USER=admin','-e','QBIT_PASS=TestOnly123','-v',f'{path}/config:/config','-v',f'{path}/downloads:/downloads','ghcr.io/stuffanthings/qbit_manage:latest')
        for name,target in [(names[1],'3000/tcp'),(names[2],'8181/tcp')]:
            port=int(docker('port',name,target).rsplit(':',1)[1])
            for attempt in range(40):
                try:
                    html=get(port,'/').decode(); assert '<html' in html.lower(); break
                except Exception:
                    if attempt==39: raise
                    time.sleep(1)
            health=json.loads(get(port,'/api/health'))
            if name==names[1]:
                assert health['ok'] and health['vpnStatus']['ok'],health
                print('PASS Gluetun dashboard HTML, read-only operation, authenticated fake-control health')
            else:
                config=json.loads(get(port,'/api/configs/config.yml'))
                assert config['data']['commands']['dry_run'] is True
                assert config['data']['qbt']['host']=='gluetun:8080'
                assert config['data']['qbt']['pass']=='!ENV QBIT_PASS',config['data']['qbt']
                config['data']['commands']['recheck']=True
                request=urllib.request.Request(f'http://127.0.0.1:{port}/api/configs/config.yml',data=json.dumps({'data':config['data']}).encode(),headers={'Content-Type':'application/json'},method='PUT')
                with urllib.request.urlopen(request,timeout=8) as response: assert response.status==200
                updated=json.loads(get(port,'/api/configs/config.yml'))
                assert updated['data']['commands']['recheck'] is True
                assert '!ENV QBIT_PASS' in (path/'config/config.yml').read_text()
                print('PASS qbit_manage dashboard HTML, starter config loading, editing/saving, !ENV preservation')
        print(json.dumps({image:docker('image','inspect',image,'--format','{{json .RepoDigests}}') for image in ['scuzza/gluetun-webui:latest','ghcr.io/stuffanthings/qbit_manage:latest']}))
    finally:
        for name in reversed(names):
            subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(['docker','network','rm',network],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
