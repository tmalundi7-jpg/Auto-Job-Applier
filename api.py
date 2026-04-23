from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import subprocess
import threading
from document_engine import generate_tailored_documents

app = Flask(__name__)
CORS(app)

DB_FILE = "jobs_database.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    return jsonify(load_db())

@app.route("/api/search", methods=["POST"])
def search_jobs():
    # Run job_manager.py in a separate thread to avoid blocking
    def run_scraper():
        print("[*] Dashboard triggered job search...")
        subprocess.run(["python", "job_manager.py"], check=True)
    
    threading.Thread(target=run_scraper).start()
    return jsonify({"status": "Search started", "message": "The job scraper is now running in the background."})

@app.route("/api/generate", methods=["POST"])
def generate_docs():
    data = request.json
    job_key = data.get("job_key")
    db = load_db()
    
    if job_key not in db:
        return jsonify({"error": "Job not found"}), 404
    
    job_details = db[job_key]
    try:
        cv_path, cl_path = generate_tailored_documents(job_details)
        return jsonify({
            "status": "Success",
            "cv_path": cv_path,
            "cl_path": cl_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
