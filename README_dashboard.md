# Find Evil Agent - Dashboard

A web dashboard built with Streamlit to visualize the results from Find Evil Agent — an autonomous cybersecurity incident response agent.

## Features
- Real-time display of suspicious activities found in logs
- Validation status (PASSED/FAILED)
- Line-level accuracy tracking for each finding
- AI investigative narrative display
- Timestamp of last analysis

## Requirements
- Python 3.12+
- Streamlit
- Find Evil Agent (agent.py) must be run first to generate report.json

## Setup

1. Clone this repository:
git clone https://github.com/ciputrii21/find-evil-agent-dashboard.git
cd find-evil-agent-dashboard

2. Create virtual environment:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:
pip install streamlit groq python-dotenv

4. Run the agent first to generate report:
python3 agent.py

5. Launch the dashboard:
streamlit run dashboard.py

6. Open browser at:
http://localhost:8501

## How It Works
1. agent.py analyzes logs and saves results to report.json
2. dashboard.py reads report.json and displays it visually
3. Dashboard auto-updates when report.json changes

## Related Project
Find Evil Agent: https://github.com/ciputrii21/find-evil-agent

## Hackathon
Built for FIND EVIL! Hackathon by SANS Institute
