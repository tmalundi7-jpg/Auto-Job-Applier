# Auto-Job-Applier - How to Run

## Quick Start

### Step 1: Open PowerShell or Command Prompt
Navigate to the project directory:
```powershell
cd C:\Users\tmalu\GitHub\Auto-Job-Applier
```

---

## Option 1: Run Job Manager (Find Job URLs)
This script searches for job URLs and saves them to the database.

```powershell
python job_manager.py
```

**What it does:**
- Launches a Chromium browser (you'll see it open)
- Searches Google for your priority jobs
- Extracts live job application URLs
- Saves URLs to `jobs_database.json`

**Expected output:**
```
[*] Launching Local Browser to find live job URLs...
[*] Searching for: Management Accountant Babcock International Dunfermline jobs
[+] Found URL: https://jobs.babcockinternational.com/...
[*] Scraping phase complete.
```

---

## Option 2: Run Auto Applier (Apply to Jobs)
This script applies to jobs using tailored documents.

```powershell
python auto_applier.py
```

**What it does:**
- Loads all jobs from the database
- Generates tailored CV and Cover Letter for each job
- Opens browser to job application portal
- Waits 5 minutes for you to manually complete the application (handles CAPTCHAs)
- Provides generated documents in `/Output` directory

**Expected output:**
```
[*] Initiating Auto-Application for: Babcock International_Management Accountant
[*] Generating targeted CV and Cover letter...
[+] Documents ready:
  - Output/Babcock International_Management Accountant_CV.pdf
  - Output/Babcock International_Management Accountant_CoverLetter.docx
[*] Navigating to https://jobs.babcockinternational.com/
[!] Reached application portal.
[!] Please complete the application manually if CAPTCHAs or Workday Logins are present.
[!] The tailored documents are in the Auto-Job-Applier/Output directory.
```

---

## Option 3: Test Document Generation
Test that documents are being created correctly.

```powershell
python document_engine.py
```

**Expected output:**
```
Loaded Master CV (text extraction logic to be implemented with pdfplumber)
Loaded Master Cover Letter (text extraction logic to be implemented with python-docx)
[*] AI Contextual Engine rewriting CV and Cover Letter for Financial Analyst at TestCorp...
```

---

## Complete Workflow

### First Time Setup:
1. **Install optional dependencies** (recommended):
   ```powershell
   pip install pdfplumber python-docx
   ```

2. **Run Job Manager** to find URLs:
   ```powershell
   python job_manager.py
   ```
   *(Takes 2-5 minutes; browser will open and close)*

3. **Check your database** got populated:
   ```powershell
   type jobs_database.json
   ```

---

### Apply to Jobs:
1. **Run Auto Applier**:
   ```powershell
   python auto_applier.py
   ```

2. **When browser opens**:
   - Fill in the application form manually
   - System will wait 5 minutes for you to complete it
   - Use the generated documents from `/Output` folder

3. **Check generated documents**:
   - Go to `Output/` folder
   - You'll find tailored CV and Cover Letter for each job

---

## File Locations

- **Project**: `C:\Users\tmalu\GitHub\Auto-Job-Applier\`
- **Master CV**: `C:\Users\tmalu\Downloads\Malundi_Christian_CV.pdf`
- **Master Cover Letter**: `C:\Users\tmalu\Downloads\Malundi_Master_Cover_Letter_Template.docx`
- **Generated Documents**: `C:\Users\tmalu\GitHub\Auto-Job-Applier\Output\`
- **Jobs Database**: `C:\Users\tmalu\GitHub\Auto-Job-Applier\jobs_database.json`

---

## Troubleshooting

### Issue: "playwright not found"
**Solution**: Install it with:
```powershell
pip install playwright
```

### Issue: "Module not found" errors
**Solution**: Install all dependencies:
```powershell
pip install -r requirements.txt
```
*(If requirements.txt doesn't exist, run the commands below)*

```powershell
pip install playwright asyncio pdfplumber python-docx
```

### Issue: Browser won't open
**Solution**: Make sure Chromium is installed for Playwright:
```powershell
playwright install
```

### Issue: "Master CV not found"
**Solution**: Ensure your files are in Downloads folder:
- `C:\Users\tmalu\Downloads\Malundi_Christian_CV.pdf`
- `C:\Users\tmalu\Downloads\Malundi_Master_Cover_Letter_Template.docx`

---

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `python job_manager.py` | Find job URLs from Google |
| `python auto_applier.py` | Apply to jobs with tailored docs |
| `python document_engine.py` | Test document generation |
| `type jobs_database.json` | View all tracked jobs |
| `dir Output/` | List generated documents |
| `pip list` | Check installed packages |
| `playwright install` | Install Chromium browser |

---

## Next Steps

1. Open PowerShell
2. Navigate to: `cd C:\Users\tmalu\GitHub\Auto-Job-Applier`
3. Run: `python job_manager.py` (or `python auto_applier.py`)
4. Watch the magic happen! 🚀
