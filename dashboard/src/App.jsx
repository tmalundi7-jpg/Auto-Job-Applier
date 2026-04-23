import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE = "http://localhost:5000/api";

function App() {
  const [jobs, setJobs] = useState([]);
  const [activeTab, setActiveTab] = useState('all');
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');

  const fetchJobs = async () => {
    try {
      // Serverless: Fetch directly from the repository's main branch
      const rawUrl = 'https://raw.githubusercontent.com/tmalundi7-jpg/Auto-Job-Applier/main/jobs_database.json';
      const resp = await fetch(rawUrl);
      if (!resp.ok) throw new Error("Could not fetch remote DB.");
      const data = await resp.json();
      setJobs(Object.entries(data).map(([key, value]) => ({ ...value, id: key })));
    } catch (err) {
      console.error("Failed to fetch jobs:", err);
      setStatusMsg("Failed to load jobs. Note: Repository must be public for serverless fetch.");
    }
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 60000); // Polling every 1m
    return () => clearInterval(interval);
  }, []);

  const triggerSearch = async () => {
    setStatusMsg('Search runs autonomously at midnight via Subagent (GitHub Actions).');
  };

  const generateDocs = async (jobKey) => {
    setStatusMsg(`Auto-generation for ${jobKey} is performed locally via document_engine.py for security.`);
  };

  const filteredJobs = activeTab === 'all' 
    ? jobs 
    : jobs.filter(j => j.category?.toLowerCase().includes(activeTab.toLowerCase()));
  
  return (
    <div className="dashboard">
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🚀</span>
          <h1>Auto-Job-Applier <span className="v-tag">v2.0 PRO</span></h1>
        </div>
        <div className="stats">
          <div className="stat-card">
            <span className="stat-value">{jobs.length}</span>
            <span className="stat-label">Total Jobs Found</span>
          </div>
          <button className="search-trigger" onClick={triggerSearch} disabled={loading}>
            {loading ? 'Searching...' : '🔍 Search UK Regions'}
          </button>
        </div>
      </header>

      {statusMsg && <div className="status-banner">{statusMsg}</div>}

      <main className="main-content">
        <section className="controls">
          <div className="tabs">
            {['all', 'accounting', 'finance', 'banking'].map(tab => (
              <button 
                key={tab}
                className={activeTab === tab ? 'tab active' : 'tab'} 
                onClick={() => setActiveTab(tab)}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
        </section>

        <section className="job-grid">
          {filteredJobs.length === 0 ? (
            <div className="empty-state">No jobs found yet. Click search to begin.</div>
          ) : (
            filteredJobs.map((job) => (
              <div key={job.id} className="job-card">
                <div className="job-header">
                  <h3>{job.role}</h3>
                  <span className={`status-badge ${job.status}`}>{job.status}</span>
                </div>
                <p className="company">{job.company} <small>via {job.source}</small></p>
                <div className="job-meta">
                  <span className="location">📍 {job.location}</span>
                  <span className="category-tag">{job.category}</span>
                </div>
                <div className="job-actions">
                  <a href={job.url} target="_blank" rel="noopener noreferrer" className="btn-primary">
                    View Portal
                  </a>
                  <button className="btn-secondary" onClick={() => generateDocs(job.id)}>
                    ✨ Tailor AI CV
                  </button>
                </div>
              </div>
            ))
          )}
        </section>
      </main>

      <footer className="footer">
        <p>Deployment Status: <span className="live-dot"></span> ANALYST SUBAGENTS ACTIVE | OLLAMA READY</p>
      </footer>
    </div>
  );
}

export default App;
