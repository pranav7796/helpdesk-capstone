import json
import collect as c
for name,args in [
    ('terraform-init-recorded',['bash','scripts/terraform-readonly.sh','init','-input=false','-lockfile=readonly','-no-color']),
    ('terraform-fmt-recorded',['bash','scripts/terraform-readonly.sh','fmt','-check','-recursive']),
    ('terraform-validate-recorded',['bash','scripts/terraform-readonly.sh','validate','-no-color']),
    ('git-status-before-docs',['git','status','--short']),
]: c.run(name,args)
pods=json.loads((c.OUT/'eks-pods.json').read_text())['items']
for p in pods:
    if p['metadata']['namespace']!='relaydesk': continue
    name=p['metadata']['name']
    if name.startswith('relaydesk-backend-'):
        c.kube('backend-replica-'+name,['-n','relaydesk','exec',name,'--','python','-c',"import os,json,urllib.request; print(json.dumps({'uid':os.getuid(),'health':json.load(urllib.request.urlopen('http://127.0.0.1:8000/health')),'ready':json.load(urllib.request.urlopen('http://127.0.0.1:8000/ready'))}))"])
    elif name.startswith('relaydesk-frontend-'):
        c.kube('frontend-replica-'+name,['-n','relaydesk','exec',name,'--','id'])
c.aws('aws-nat-retry',['ec2','describe-nat-gateways','--filter','Name=vpc-id,Values=vpc-0f1334a144012db46'])
c.kube('eks-top-nodes-recorded',['top','nodes'])
for role in ['relaydesk-capstone-cluster-role','relaydesk-capstone-nodes-role','relaydesk-capstone-ebs-csi-role']:
    c.aws('iam-'+role,['iam','list-attached-role-policies','--role-name',role])
(c.OUT/'supplement-results.json').write_text(json.dumps(c.records,indent=2)+'\n')
