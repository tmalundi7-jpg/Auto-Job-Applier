import subprocess
import os
import sys

def main():
    print("[ScoutAgent] Initializing high-priority job scouting...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    job_manager_path = os.path.join(project_root, "job_manager.py")
    
    if not os.path.exists(job_manager_path):
        print(f"[ScoutAgent] Error: {job_manager_path} not found.")
        return

    print(f"[ScoutAgent] Executing {job_manager_path}...")
    try:
        # We run with the same python interpreter
        result = subprocess.run([sys.executable, job_manager_path], check=True)
        print("[ScoutAgent] Job scouting complete.")
    except subprocess.CalledProcessError as e:
        print(f"[ScoutAgent] Execution failed: {e}")

if __name__ == "__main__":
    main()
