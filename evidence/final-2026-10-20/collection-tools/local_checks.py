import json, urllib.request, urllib.error, uuid
import collect as c
records=[]
def call(path,method='GET',data=None):
    req=urllib.request.Request('http://127.0.0.1:3000'+path,method=method,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=20) as response:
        status=response.status; raw=response.read(); records.append({'method':method,'path':path,'status':status}); return status,json.loads(raw) if raw else None
ticket={'subject':'Disposable local final audit '+str(uuid.uuid4()),'requester':'Audit','priority':'HIGH'}
_,before=call('/api/tickets'); ident=None
try:
    status,saved=call('/api/tickets','POST',ticket); assert status==201;ident=saved['id']
    status,saved=call('/api/tickets/'+str(ident)); assert status==200
    status,saved=call('/api/tickets/'+str(ident),'PUT',{**ticket,'status':'RESOLVED'});assert status==200 and saved['status']=='RESOLVED'
finally:
    if ident is not None: assert call('/api/tickets/'+str(ident),'DELETE')[0]==204
_,after=call('/api/tickets');assert before==after
(c.OUT/'compose-crud.json').write_text(json.dumps({'result':'PASS','preexisting_records_preserved':True,'requests':records},indent=2)+'\n')
c.run('compose-status-final',['docker','compose','ps','-a','--format','json'])
for service in ['backend','frontend']:
    c.run('compose-uid-'+service,['docker','compose','exec','-T',service,'id'])
c.run('compose-postgres',['docker','compose','exec','-T','postgres','sh','-c','psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT version_num FROM alembic_version;" -c "SELECT count(*) AS tickets FROM tickets;"'])
(c.OUT/'local-check-results.json').write_text(json.dumps(c.records,indent=2)+'\n')
print('PASS local Compose CRUD; preexisting records preserved',flush=True)
