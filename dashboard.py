import streamlit as st
import json
import os

st.set_page_config(page_title="Find Evil Agent", page_icon="🔍", layout="wide")

st.title("🔍 Find Evil Agent Dashboard")
st.markdown("**Autonomous Cybersecurity Incident Response Agent**")

st.divider()

if os.path.exists("report.json"):
    with open("report.json", "r") as f:
        report = json.load(f)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Suspicious", report["findings"]["total_suspicious"])
    with col2:
        st.metric("Validation", "PASSED" if report["validation"]["is_valid"] else "FAILED")
    with col3:
        st.metric("Timestamp", report["timestamp"][:10])

    st.subheader("🚨 Suspicious Activities Found")
    for finding in report["findings"]["findings"]:
        st.error(f"Line {finding['line_number']}: {finding['content']} [keyword: {finding['keyword_matched']}]")

    st.subheader("🤖 AI Investigative Narrative")
    st.markdown(report["ai_analysis"])

else:
    st.warning("No report found. Run agent.py first!")
    st.code("python3 agent.py")
