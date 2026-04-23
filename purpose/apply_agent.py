import subprocess
import os
import sys

def main():
    print("[ApplyAgent] Initializing automated application process...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    auto_applier_path = os.path.join(project_root, "auto_applier.py")
    
    if not os.path.exists(auto_applier_path):
        print(f"[ApplyAgent] Error: {auto_applier_path} not found.")
        return

    print(f"[ApplyAgent] Executing {auto_applier_path}...")
    try:
        # We run with the same python interpreter
        # Note: This will launch a browser window.
        result = subprocess.run([sys.executable, auto_applier_path], check=True)
        print("[ApplyAgent] Job applications processed.")
    except subprocess.CalledProcessError as e:
        print(f"[ApplyAgent] Execution failed: {e}")

if __name__ == "__main__":
    main()
