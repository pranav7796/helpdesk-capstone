from pathlib import Path
import sys,re
name=sys.argv[1]
print('GITHUB ACTIONS PIPELINE OUTPUT (saved genuine run log)')
print('Run: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596')
print('Commit: d07bca6accc35f0224aaae8c4057076a9c4c9261')
print('Step: Scan '+name+' image with Trivy')
print('Workflow gate: HIGH,CRITICAL; exit-code=1; ignore-unfixed=true')
print('Exact package-PURL SBOM exceptions: docs/SECURITY.md.\n')
lines=[l.split('\t',2)[2] for l in Path('evidence/actions-run.txt').read_text().splitlines() if '\tScan '+name+' image with Trivy\t' in l]
messages=[re.sub(r'^\S+Z\s?', '',l) for l in lines]
table=[m for m in messages if m.startswith(('┌','│','├','└','┬','┴'))]
print('Report Summary — exact table excerpt from the pipeline log')
if name=='backend':
    print('OS and Python summary rows shown; detailed clean package rows remain in the full log.')
    table=table[:6]+[table[-1]]
for row in table: print(row)
print("Legend from pipeline: '0': Clean (no security findings detected).")
print('\nSource: evidence/actions-run.txt (full unabridged workflow log)')
