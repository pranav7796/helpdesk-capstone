import concurrent.futures, datetime, json, os, pathlib, re, subprocess, time
ROOT = pathlib.Path('/home/pranav/Projects/helpdesk-capstone')
OUT = pathlib.Path('/tmp/relaydesk-audit-2026-10-20/results')
OUT.mkdir(exist_ok=True)
ENV = dict(os.environ, AWS_PROFILE='devops-new', AWS_REGION='ap-southeast-2', AWS_DEFAULT_REGION='ap-southeast-2', AWS_PAGER='', KUBECONFIG=str(ROOT/'evidence/private/kubeconfig-sydney'), PYTHONDONTWRITEBYTECODE='1')
secrets = []
for filename in ['eks-values.json', 'grafana-admin.json']:
    d = json.loads((ROOT/'evidence/private'/filename).read_text())
    secrets.append(d.get('database', {}).get('password') or d.get('stringData', {}).get('password'))
def clean(text):
    for value in secrets:
        if value: text = text.replace(value, '[REDACTED]')
    return re.sub(r'postgres(?:ql)?(?:\+psycopg)?://[^\s"\x27]+', '[REDACTED_DATABASE_URL]', text)
def strip_annotations(obj):
    if isinstance(obj, dict):
        return {k: strip_annotations(v) for k,v in obj.items() if k not in ['kubectl.kubernetes.io/last-applied-configuration', 'managedFields']}
    if isinstance(obj,list): return [strip_annotations(x) for x in obj]
    return obj
records=[]
def run(name,args,timeout=90,cwd=ROOT):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        r=subprocess.run(args,env=ENV,cwd=cwd,text=True,capture_output=True,timeout=timeout)
        stdout=clean(r.stdout); stderr=clean(r.stderr); code=r.returncode
    except subprocess.TimeoutExpired as e:
        stdout=clean((e.stdout or b'').decode() if isinstance(e.stdout,bytes) else e.stdout or '')
        stderr='TIMEOUT'; code=124
    is_json=False
    try:
        try: parsed=json.loads(stdout)
        except ValueError: parsed=[json.loads(line) for line in stdout.splitlines() if line.strip()]; assert parsed
        stdout=json.dumps(strip_annotations(parsed),indent=2)+'\n'; is_json=True
    except (ValueError,TypeError,AssertionError): pass
    suffix='.json' if is_json else '.txt'
    (OUT/(name+suffix)).write_text(stdout)
    rec=dict(name=name,command=args,cwd=str(cwd),started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=code,stdout=name+suffix,stderr=stderr)
    records.append(rec)
    print(name,code,stderr[:160],flush=True)
    return json.loads(stdout) if code==0 and suffix=='.json' else None
def aws(name,args): return run(name,['aws',*args,'--profile','devops-new','--region','ap-southeast-2','--output','json','--no-cli-pager'])
K=['kubectl','--context','relaydesk-sydney','--request-timeout=12s']
def kube(name,args): return run(name,K+args,timeout=45)
def cloud():
    aws('aws-identity',['sts','get-caller-identity'])
    aws('aws-eks',['eks','describe-cluster','--name','relaydesk-capstone'])
    aws('aws-nodegroup',['eks','describe-nodegroup','--cluster-name','relaydesk-capstone','--nodegroup-name','relaydesk-capstone-workers'])
    addons=aws('aws-addons',['eks','list-addons','--cluster-name','relaydesk-capstone'])
    for addon in (addons or {}).get('addons',[]): aws('aws-addon-'+addon,['eks','describe-addon','--cluster-name','relaydesk-capstone','--addon-name',addon])
    for name,service,operation,filters in [
        ('vpc','ec2','describe-vpcs',['Name=vpc-id,Values=vpc-0f1334a144012db46']),
        ('subnets','ec2','describe-subnets',['Name=vpc-id,Values=vpc-0f1334a144012db46']),
        ('routes','ec2','describe-route-tables',['Name=vpc-id,Values=vpc-0f1334a144012db46']),
        ('nat','ec2','describe-nat-gateways',['Name=vpc-id,Values=vpc-0f1334a144012db46']),
        ('workers','ec2','describe-instances',['Name=tag:eks:cluster-name,Values=relaydesk-capstone','Name=instance-state-name,Values=running']),
        ('security-groups','ec2','describe-security-groups',['Name=vpc-id,Values=vpc-0f1334a144012db46']),
    ]: aws('aws-'+name,[service,operation,'--filters',*filters])
    aws('aws-volumes',['ec2','describe-volumes','--volume-ids','vol-05a891d9a7dce0955','vol-059e7140240f20306','vol-0c2635d6fa9ef9ce2'])
    aws('aws-elb',['elb','describe-load-balancers','--load-balancer-names','af43a3e33d68945548232885350507ff'])
    aws('aws-elb-health',['elb','describe-instance-health','--load-balancer-name','af43a3e33d68945548232885350507ff'])
    aws('aws-pod-identity',['eks','list-pod-identity-associations','--cluster-name','relaydesk-capstone'])
def cluster():
    for name,args in [
        ('eks-nodes',['get','nodes','-o','json']),
        ('eks-pods',['get','pods','-A','-o','json']),
        ('eks-runtime',['-n','relaydesk','get','deploy,sts,svc,hpa,pvc,ingress','-o','json']),
        ('eks-endpoints',['-n','relaydesk','get','endpointslices','-o','json']),
        ('eks-events',['get','events','-A','--sort-by=.lastTimestamp','-o','json']),
        ('eks-storage',['get','pv,storageclass','-o','json']),
        ('eks-ingress',['-n','ingress-system','get','deploy,svc,pods','-o','json']),
        ('eks-monitoring-config',['-n','relaydesk','get','cm','prometheus-config','grafana-dashboard','grafana-datasource','-o','json']),
        ('eks-top-nodes',['top','nodes']),
        ('eks-top-pods',['-n','relaydesk','top','pods']),
        ('eks-namespace-dryrun',['apply','--dry-run=server','-f','k8s/namespace.yaml']),
        ('promtool',['-n','relaydesk','exec','deploy/prometheus','--','promtool','check','config','/etc/prometheus/prometheus.yml']),
        ('postgres-schema',['-n','relaydesk','exec','relaydesk-postgres-0','--','sh','-c','psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT version_num FROM alembic_version;" -c "SELECT count(*) AS tickets FROM tickets;" -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = \'tickets\' ORDER BY ordinal_position;"']),
    ]: kube(name,args)
    pods=json.loads((OUT/'eks-pods.json').read_text()).get('items',[])
    for p in pods:
        ns=p['metadata']['namespace']; name=p['metadata']['name']
        if ns not in ('relaydesk','ingress-system'): continue
        for c in p['spec'].get('containers',[])+p['spec'].get('initContainers',[]):
            kube('logs-'+name+'-'+c['name'],['-n',ns,'logs',name,'-c',c['name'],'--since=30m','--tail=100'])
    run('helm-list',['helm','--kube-context','relaydesk-sydney','list','-A','-o','json'])
    run('helm-history',['helm','--kube-context','relaydesk-sydney','history','relaydesk','-n','relaydesk','-o','json'])
def local():
    for name,args in [
        ('pytest',['backend/.venv/bin/pytest','-v','-p','no:cacheprovider','--junitxml='+str(OUT/'pytest.xml'),'backend/tests']),
        ('frontend-build',['npm','--prefix','frontend','run','build']),
        ('helm-local-lint',['helm','lint','helm/helpdesk','-f','helm/helpdesk/values-local.yaml']),
        ('helm-eks-lint',['helm','lint','helm/helpdesk','-f','helm/helpdesk/values-eks.yaml']),
        ('monitoring-render',['kubectl','kustomize','monitoring']),
        ('compose-status',['docker','compose','ps','--format','json']),
        ('git-history',['git','log','--format=%h %s','-20']),
        ('github-repository',['gh','repo','view','pranav7796/helpdesk-capstone','--json','url,visibility,defaultBranchRef']),
        ('github-runs',['gh','run','list','--repo','pranav7796/helpdesk-capstone','--limit','5','--json','databaseId,headSha,status,conclusion,url,createdAt']),
    ]: run(name,args,timeout=120)
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(fn) for fn in (cloud,cluster,local)]
        for f in futures:
            try: f.result()
            except Exception as e: records.append({'collector_error':type(e).__name__+': '+str(e)}); print(type(e).__name__,str(e),flush=True)
    (OUT/'collection-results.json').write_text(json.dumps(records,indent=2)+'\n')
