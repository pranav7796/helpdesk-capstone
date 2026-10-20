import datetime, hashlib, importlib.util, json, pathlib, re, subprocess
import collect as c
R,O=c.ROOT,c.OUT
spec=importlib.util.spec_from_file_location('existing_audit', R/'scripts/audit-evidence.py')
audit=importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)
old=json.loads((R/'evidence/final-2026-10-17/evidence-audit.json').read_text())
errors=[]; screenshots=[]; videos=[]
for x in old['screenshots']:
    path=R/x['screenshot']
    try:
        assert audit.digest(path)==x['sha256']
        screenshots.append({'path':x['screenshot'],'sha256':x['sha256'],**audit.png(path),'review_basis':'Existing recorded visual review; hash unchanged'})
    except Exception as e: errors.append({'path':str(path),'error':type(e).__name__})
actual={str(p.relative_to(R)) for p in (R/'evidence/screenshots').glob('*.png')}
assert actual=={x['path'] for x in screenshots}
for x in old['videos']:
    path=R/x['path']
    try:
        assert audit.digest(path)==x['sha256']
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height','-of','json',str(path)],text=True))
        assert float(probe['format']['duration'])>0
        videos.append({'path':x['path'],'sha256':x['sha256'],'probe':probe,'review_basis':'Existing timeline/review; hash unchanged'})
    except Exception as e: errors.append({'path':str(path),'error':str(e)})
public_json=0
for p in (R/'evidence').rglob('*.json'):
    if 'private' in p.relative_to(R/'evidence').parts: continue
    try: json.loads(p.read_text()); public_json+=1
    except Exception as e: errors.append({'path':str(p.relative_to(R)),'error':str(e)})
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
inventory=[]; sensitive=[]
pattern=re.compile(rb'(?:AKIA|ASIA)[A-Z0-9]{16}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----')
for name in filter(None,tracked):
    p=R/name
    data=p.read_bytes()
    if pattern.search(data) or any(s and s.encode() in data for s in c.secrets): sensitive.append(name)
    if not name.startswith('evidence/'):
        inventory.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'text':b'\0' not in data})
ignore=[]
for name in ['.env','backend/__pycache__/check.pyc','frontend/node_modules/check','backend/.venv/check','terraform/terraform.tfvars','terraform/terraform.tfstate','terraform/test.tfplan','evidence/private/kubeconfig-sydney']:
    rc=subprocess.run(['git','check-ignore','-q',name],cwd=R).returncode
    ignore.append({'path':name,'ignored':rc==0})
assert not sensitive and all(x['ignored'] for x in ignore)
commits=subprocess.check_output(['git','rev-list','--all'],cwd=R,text=True).splitlines()
history_findings=[]
for commit in commits:
    r=subprocess.run(['git','grep','-I','-l','-E',r'(AKIA|ASIA)[A-Z0-9]{16}|-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----',commit],cwd=R,capture_output=True,text=True)
    if r.returncode not in (0,1): errors.append({'history_scan_error':commit})
    if r.returncode==0: history_findings.extend(r.stdout.splitlines())
criteria=json.loads((R/'evidence/final-2026-10-17/criterion-evidence.json').read_text())
assert len(criteria)==46 and sum(x['points'] for x in criteria)==100
for row in criteria:
    for name in row['screenshots']: assert (R/name).is_file()
report={'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'screenshots_validated':len(screenshots),'videos_validated':len(videos),'public_json_parsed':public_json,'criteria_references_checked':len(criteria),'errors':errors,'screenshots':screenshots,'videos':videos,'scope':'Hashes/PNG CRCs/decompression/video metadata checked freshly. Visual review and authenticity rely on preserved capture provenance; no fresh UI screenshot or recording was captured.'}
(O/'evidence-integrity.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'source-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
(O/'git-hygiene.json').write_text(json.dumps({'tracked_files':len(list(filter(None,tracked))),'non_evidence_files_read':len(inventory),'sensitive_signature_or_known_password_paths':sensitive,'ignore_checks':ignore,'history_commits_scanned':len(commits),'history_signature_matches':history_findings,'limitation':'Signature-based check and known private passwords; not a comprehensive secret-security certification.'},indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['screenshots','videos']},indent=2)); print('history signature matches:',len(history_findings),'source files:',len(inventory))
assert not errors and not history_findings
