import asyncio
import json
import os
from playwright.async_api import async_playwright
import document_engine

DB_FILE = "jobs_database.json"

def load_jobs():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

async def apply_to_job(job_key, job_data, p):
    url = job_data.get("url")
    if not url or "http" not in url:
        print(f"[-] Invalid URL for {job_key}")
        return
    
    print(f"\n[*] Initiating Auto-Application for: {job_key}")
    
    # 1. Generate tailored documents
    print("[*] Generating targeted CV and Cover letter...")
    cv_path, cl_path = document_engine.generate_tailored_documents(job_data)
    print(f"[+] Documents ready:\n  - {cv_path}\n  - {cl_path}")

    # 2. Launch browser for the application process
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    
    print(f"[*] Navigating to {url}")
    try:
        await page.goto(url, timeout=60000)
        
        # In a generic auto-applier, we would look for common button text like "Apply Now", "Apply Online"
        # Since ATS portals are highly variable (Workday, SuccessFactors), we stop here and allow
        # the user to take over the session (Copilot Mode)
        print("[!] Reached application portal.")
        print("[!] Please complete the application manually if CAPTCHAs or Workday Logins are present.")
        print("[!] The tailored documents are in the Auto-Job-Applier/Output directory.")
        
        # Keep browser open for user to complete
        await page.wait_for_timeout(300000) # 5 minutes pause
        
    except Exception as e:
        print(f"[-] Error navigating to application portal: {e}")
        
    await browser.close()

async def main():
    jobs = load_jobs()
    if not jobs:
        print("[-] No jobs in database to apply to. Run job_manager.py first.")
        return
        
    async with async_playwright() as p:
        for key, details in jobs.items():
            if details.get("status") == "URL_FOUND":
                await apply_to_job(key, details, p)

if __name__ == "__main__":
    asyncio.run(main())
