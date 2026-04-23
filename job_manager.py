import json
import os
import asyncio
import random
from playwright.async_api import async_playwright

DB_FILE = "jobs_database.json"

UK_REGIONS = [
    "London", "South East", "South West", "West Midlands", "East Midlands", 
    "East of England", "North West", "North East", "Yorkshire and The Humber",
    "Scotland", "Wales", "Northern Ireland"
]

TARGET_ROLES = [
    "Financial Analyst", "Audit Associate", "Investment Banking Analyst",
    "Management Accountant", "Finance Manager", "Senior Accountant",
    "Tax Associate", "Fund Accountant", "Compliance Officer"
]

JOB_ENGINES = [
    {"name": "LinkedIn", "url": "https://www.linkedin.com/jobs/search/?keywords={query}&location={location}"},
    {"name": "Indeed", "url": "https://uk.indeed.com/jobs?q={query}&l={location}"},
    {"name": "Reed", "url": "https://www.reed.co.uk/jobs/{query}-jobs-in-{location}"},
    {"name": "Totaljobs", "url": "https://www.totaljobs.com/jobs/{query}/in-{location}"}
]

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def scrape_job_links():
    print("[*] Starting UK-Wide Multi-Engine Job Search...")
    async with async_playwright() as p:
        is_ci = os.getenv("CI", "false").lower() == "true"
        browser = await p.chromium.launch(headless=is_ci) # Headless if in CI, Headed if local
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        db = load_db()
        
        # We sample categories to keep the demo/run time reasonable but comprehensive
        for role in random.sample(TARGET_ROLES, 3): 
            for region in UK_REGIONS:
                for engine in JOB_ENGINES:
                    query = role.replace(" ", "%20")
                    location = region.replace(" ", "%20")
                    search_url = engine["url"].format(query=query, location=location)
                    
                    print(f"[*] Searching {engine['name']} for {role} in {region}...")
                    try:
                        await page.goto(search_url, timeout=30000)
                        await asyncio.sleep(random.uniform(2, 5)) # Human-like delay
                        
                        # Handle common cookie popups
                        try:
                            if "indeed" in search_url:
                                await page.click('button[id="onetrust-accept-btn-handler"]', timeout=2000)
                            elif "linkedin" in search_url:
                                await page.click('button[data-tracking-control-name="public_jobs_contextual-sign-in-modal_modal_dismiss"]', timeout=2000)
                        except:
                            pass

                        # Extract first meaningful job link
                        links = await page.evaluate('''() => {
                            const results = [];
                            const anchors = Array.from(document.querySelectorAll('a'));
                            for (let a of anchors) {
                                const href = a.href;
                                if (href.includes("/jobs/") || href.includes("/view/") || href.includes("-jobs")) {
                                    if (!href.includes("google") && !href.includes("facebook") && href.startsWith("http")) {
                                        results.push({
                                            url: href,
                                            text: a.innerText.trim()
                                        });
                                    }
                                }
                            }
                            return results;
                        }''')

                        if links:
                            job_data = links[0]
                            key = f"{engine['name']}_{role}_{region}".replace(" ", "_")
                            db[key] = {
                                "company": "Various", # Scraping exact company name requires more specific selectors per engine
                                "role": role,
                                "location": region,
                                "url": job_data["url"],
                                "source": engine["name"],
                                "status": "URL_FOUND",
                                "category": "Finance/Accounting"
                            }
                            save_db(db)
                            print(f"[+] Found on {engine['name']}: {job_data['url'][:50]}...")
                    
                    except Exception as e:
                        print(f"[-] Error searching {engine['name']} in {region}: {e}")
                        continue
                        
        await browser.close()
        print("[*] Multi-engine search complete.")

if __name__ == "__main__":
    asyncio.run(scrape_job_links())
