import base64, datetime, hashlib, json, pathlib, time, urllib.error, urllib.parse, urllib.request, uuid
import collect as c
O=c.OUT
HOST='http://af43a3e33d68945548232885350507ff-719760255.ap-southeast-2.elb.amazonaws.com'
records=[]
def call(name,url,method='GET',data=None,headers=None,save_body=False):
    req=urllib.request.Request(url,method=method,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json',**(headers or {})})
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req,timeout=20) as r: status=r.status; body=r.read(); content=r.headers.get('Content-Type','')
    except urllib.error.HTTPError as e: status=e.code; body=e.read(); content=e.headers.get('Content-Type','')
    rec=dict(name=name,url=url,method=method,status=status,content_type=content,captured_at_utc=started,body_sha256=hashlib.sha256(body).hexdigest())
    records.append(rec)
    if save_body: (O/(name+('.json' if 'json' in content else '.txt'))).write_text(c.clean(body.decode()))
    print(name,status,content,flush=True)
    try: return status,json.loads(body)
    except ValueError: return status,body.decode()
def query(name,expr):
    status,data=call(name,'http://127.0.0.1:9091/api/v1/query?'+urllib.parse.urlencode({'query':expr}),save_body=True)
    assert status==200 and data['status']=='success'
    return data['data']['result']
audit_id=None
try:
    code,html=call('ingress-frontend',HOST+'/',save_body=True); assert code==200 and 'id="root"' in html
    import re
    assets=re.findall(r'(?:src|href)="(/assets/[^\"]+)"',html)
    assert assets
    for i,path in enumerate(assets):
        code,body=call('frontend-asset-'+str(i),HOST+path); assert code==200
    for route,value in [('health','UP'),('ready','READY')]:
        code,body=call('backend-'+route,'http://127.0.0.1:8001/'+route,save_body=True); assert code==200 and body['status']==value
    code,body=call('backend-metrics','http://127.0.0.1:8001/metrics',save_body=True); assert code==200 and 'relaydesk_http_requests_total' in body
    code,before=call('ingress-tickets-before',HOST+'/api/tickets'); assert code==200 and isinstance(before,list)
    (O/'ticket-count-before.json').write_text(json.dumps({'count':len(before),'ids':[x['id'] for x in before]},indent=2)+'\n')
    ticket={'subject':'Disposable final audit '+str(uuid.uuid4()),'requester':'Submission audit','description':'Synthetic verification record; removed by this audit.','assignee':'Audit','priority':'HIGH','status':'OPEN'}
    code,row=call('crud-create',HOST+'/api/tickets','POST',ticket); assert code==201 and row['subject']==ticket['subject']; audit_id=row['id']
    code,row=call('crud-get',HOST+'/api/tickets/'+str(audit_id)); assert code==200 and row['status']=='OPEN'
    ticket.update(status='IN_PROGRESS',priority='URGENT')
    code,row=call('crud-update',HOST+'/api/tickets/'+str(audit_id),'PUT',ticket); assert code==200 and row['status']=='IN_PROGRESS' and row['priority']=='URGENT'
    code,rows=call('crud-filter',HOST+'/api/tickets?status=IN_PROGRESS'); assert code==200 and any(x['id']==audit_id for x in rows) and all(x['status']=='IN_PROGRESS' for x in rows)
    c.kube('postgres-audit-row',['-n','relaydesk','exec','relaydesk-postgres-0','--','sh','-c',f'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT id, status, priority FROM tickets WHERE id = {audit_id};"'])
    assert 'IN_PROGRESS' in (O/'postgres-audit-row.txt').read_text()
    code,_=call('crud-invalid-input',HOST+'/api/tickets','POST',{}); assert code==422
    code,_=call('crud-delete',HOST+'/api/tickets/'+str(audit_id),'DELETE'); assert code==204
    code,_=call('crud-deleted-404',HOST+'/api/tickets/'+str(audit_id)); assert code==404
    deleted=audit_id; audit_id=None
    code,after=call('ingress-tickets-after',HOST+'/api/tickets'); assert code==200 and not any(x['id']==deleted for x in after)
    (O/'crud-summary.json').write_text(json.dumps({'result':'PASS','synthetic_ticket_id':deleted,'synthetic_ticket_deleted':True,'initial_ids':[x['id'] for x in before],'final_ids':[x['id'] for x in after],'preexisting_records_preserved':all(x in after for x in before)},indent=2)+'\n')
    code,health=call('prometheus-ready','http://127.0.0.1:9091/-/ready',save_body=True); assert code==200
    code,targets=call('prometheus-targets','http://127.0.0.1:9091/api/v1/targets',save_body=True); assert code==200
    apps=[t for t in targets['data']['activeTargets'] if t['labels'].get('job')=='relaydesk-backend']
    assert len(apps)==2 and all(t['health']=='up' and t['labels'].get('scrape_mode')=='pod' and not t['lastError'] for t in apps)
    assert len({t['scrapeUrl'] for t in apps})==2
    up=query('prometheus-up','up{job="relaydesk-backend",scrape_mode="pod"}'); assert len(up)==2 and all(x['value'][1]=='1' for x in up)
    rates=query('prometheus-rates','sum by (route) (rate(relaydesk_http_requests_total{job="relaydesk-backend",scrape_mode="pod"}[2m]))'); assert any(float(x['value'][1])>0 for x in rates)
    query('prometheus-resets','resets(relaydesk_http_requests_total{job="relaydesk-backend",scrape_mode="pod"}[5m])')
    code,health=call('grafana-health','http://127.0.0.1:3002/api/health',save_body=True); assert code==200 and health['database']=='ok'
    password=json.loads((c.ROOT/'evidence/private/grafana-admin.json').read_text())['stringData']['password']
    headers={'Authorization':'Basic '+base64.b64encode(('admin:'+password).encode()).decode()}
    code,d=call('grafana-dashboard','http://127.0.0.1:3002/api/dashboards/uid/relaydesk-http',headers=headers,save_body=True); assert code==200 and d['dashboard']['panels']
    code,ds=call('grafana-datasource-health','http://127.0.0.1:3002/api/datasources/uid/prometheus/health',headers=headers,save_body=True); assert code==200 and ds['status']=='OK'
    expr=d['dashboard']['panels'][0]['targets'][0]['expr']
    now=int(time.time()*1000)
    payload={'from':str(now-300000),'to':str(now),'queries':[{'refId':'A','expr':expr,'range':True,'instant':False,'datasource':{'type':'prometheus','uid':'prometheus'},'intervalMs':15000,'maxDataPoints':300}]}
    code,result=call('grafana-panel-query','http://127.0.0.1:3002/api/ds/query','POST',payload,headers,save_body=True)
    assert code==200
    frames=result['results']['A']['frames']; assert frames and any(any(isinstance(v,(int,float)) and v>0 for v in f['data']['values'][1]) for f in frames)
    print('PASS: ingress CRUD, PostgreSQL persistence, health/readiness/metrics, two UP scrape targets, authenticated Grafana panel query with positive data',flush=True)
finally:
    if audit_id is not None:
        call('cleanup-disposable-audit-row',HOST+'/api/tickets/'+str(audit_id),'DELETE')
    (O/'http-check-results.json').write_text(json.dumps(records,indent=2)+'\n')
    (O/'http-kube-results.json').write_text(json.dumps(c.records,indent=2)+'\n')
