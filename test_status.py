import json
import os

# Verify database
db_file = 'jobs_database.json'
with open(db_file, 'r') as f:
    db = json.load(f)
    
print('[+] Jobs Database Status:')
print(f'    Total jobs: {len(db)}')
for key, job in db.items():
    status = job.get('status', 'UNKNOWN')
    has_url = 'url' in job and job['url']
    company = job.get('company', 'Unknown')
    print(f'    - {company}: {status} | URL: {"YES" if has_url else "NO"}')

# Verify output directory
output_dir = 'Output'
if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    print(f'[+] Output Directory: {len(files)} generated documents')
else:
    print('[-] Output directory not found')

# Verify master documents
cv_path = r'C:\Users\tmalu\Downloads\Malundi_Christian_CV.pdf'
cl_path = r'C:\Users\tmalu\Downloads\Malundi_Master_Cover_Letter_Template.docx'
print(f'[+] Master CV exists: {os.path.exists(cv_path)}')
print(f'[+] Master Cover Letter exists: {os.path.exists(cl_path)}')
