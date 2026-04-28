Find Evil Agent - Dashboard
A web dashboard built with Streamlit to visualize the results from Find Evil Agent — an autonomous cybersecurity incident response agent.

Features
Real-time display of suspicious activities found in logs
Validation status (PASSED/FAILED)
Line-level accuracy tracking for each finding
AI investigative narrative display
Timestamp of last analysis
Requirements
Python 3.12+
Streamlit
Find Evil Agent (agent.py) must be run first to generate report.json
Setup
Clone this repository: git clone https://github.com/ciputrii21/find-evil-agent-dashboard.git cd find-evil-agent-dashboard

Create virtual environment: python3 -m venv venv source venv/bin/activate

Install dependencies: pip install streamlit groq python-dotenv

Run the agent first to generate report: python3 agent.py

Launch the dashboard: streamlit run dashboard.py

Open browser at: http://localhost:8501

How It Works
agent.py analyzes logs and saves results to report.json
dashboard.py reads report.json and displays it visually
Dashboard auto-updates when report.json changes
Related Project
Find Evil Agent: https://github.com/ciputrii21/find-evil-agent

Hackathon
Built for FIND EVIL! Hackathon by SANS Institute
