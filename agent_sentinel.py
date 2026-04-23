import json
import os
import time

DB_FILE = "jobs_database.json"

def monitor():
    print("[SentinelAgent] Monitoring Auto-Job-Applier status...")
    while True:
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r") as f:
                    db = json.load(f)
                
                total = len(db)
                found = sum(1 for j in db.values() if j.get("status") == "URL_FOUND")
                applied = sum(1 for j in db.values() if j.get("status") == "APPLIED") # hypothetical status
                
                print(f"[SentinelAgent] Status Update: {total} jobs tracked | {found} ready | {applied} applied")
                
                # Check for common issues (e.g. invalid URLs)
                for key, data in db.items():
                    if "url" in data and ("http" not in data["url"]):
                        print(f"[SentinelAgent] Warning: Invalid URL for {key}")
                
            except Exception as e:
                print(f"[SentinelAgent] Error reading database: {e}")
        else:
            print("[SentinelAgent] Database not found yet.")
        
        # In a real 24/7 deployment, this would be a long sleep
        print("[SentinelAgent] Sleeping for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    monitor()
