import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ============================================================
# TOOL 1: Analyze log with line tracking
# ============================================================
def analyze_log(log_text: str) -> dict:
    """Analyzes log and tracks exact line numbers for each finding."""
    suspicious = []
    keywords = ["failed", "error", "unauthorized", "attack", "malware", "suspicious"]
    
    for line_num, line in enumerate(log_text.split("\n"), 1):
        for keyword in keywords:
            if keyword.lower() in line.lower() and line.strip():
                suspicious.append({
                    "line_number": line_num,
                    "content": line.strip(),
                    "keyword_matched": keyword
                })
                break
    return {
        "total_suspicious": len(suspicious),
        "findings": suspicious
    }

# ============================================================
# TOOL 2: Self-correction validator
# ============================================================
def validate_findings(findings: dict, ai_response: str) -> dict:
    """Validates AI response against actual log findings."""
    errors = []
    
    if findings["total_suspicious"] == 0 and "suspicious" in ai_response.lower():
        errors.append("AI claimed suspicious activity but none found in log")
    
    if findings["total_suspicious"] > 0 and "no threat" in ai_response.lower():
        errors.append("AI missed detected threats")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

# ============================================================
# MAIN AGENT with self-correction
# ============================================================
def run_agent(log_text: str, max_retries: int = 3):
    """Main agent with self-correction capability."""
    
    print("=" * 50)
    print("FIND EVIL AGENT v2.0")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Step 1: Analyze log
    print("\n[STEP 1] Running log analysis tool...")
    findings = analyze_log(log_text)
    print(f"[Tool: analyze_log] Found {findings['total_suspicious']} suspicious activities")
    
    for f in findings["findings"]:
        print(f"  -> Line {f['line_number']}: {f['content']} [keyword: {f['keyword_matched']}]")
    
    # Step 2: AI reasoning with retry
    print("\n[STEP 2] Agent reasoning...")
    
    findings_text = "\n".join([
        f"Line {f['line_number']}: {f['content']}"
        for f in findings["findings"]
    ])
    
    prompt = f"""You are a cybersecurity incident response agent.

Log analysis found {findings['total_suspicious']} suspicious activities:
{findings_text}

Provide a structured investigative narrative including:
1. Threat Assessment (reference specific line numbers)
2. Affected Systems
3. Recommended Response Actions
4. Confidence Level (0-100%)

Always reference line numbers when citing evidence."""

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        print(f"\n[Attempt {attempt}/{max_retries}] Calling AI...")
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_result = response.choices[0].message.content
            
            # Step 3: Validate
            print("[STEP 3] Validating findings...")
            validation = validate_findings(findings, ai_result)
            
            if validation["is_valid"]:
                print("[✓] Validation passed!")
                break
            else:
                print(f"[✗] Validation failed: {validation['errors']}")
                print("[Self-correction] Retrying with corrected prompt...")
                prompt += f"\n\nPrevious response had errors: {validation['errors']}. Please correct."
                time.sleep(2)
                
        except Exception as e:
            print(f"[Error] {e}")
            time.sleep(3)
    
    # Step 4: Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "findings": findings,
        "ai_analysis": ai_result,
        "validation": validation
    }
    
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 50)
    print("INVESTIGATIVE NARRATIVE")
    print("=" * 50)
    print(ai_result)
    print("\n[✓] Report saved to report.json")
    print("=== ANALYSIS COMPLETE ===")
    
    return report

# Test
log_sample = """
failed login attempt from 192.168.1.1
normal system boot completed
system error occurred in auth module
unauthorized access detected on port 22
user john logged in successfully
malware signature detected in process 1234
suspicious outbound connection to 10.0.0.99
"""

run_agent(log_sample)
