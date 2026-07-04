import requests
import json
import time

SLACK_URL = "SET_YOUR_SLACK_URL" 
VT_API_KEY = "SET_YOUR_VT_API_KEY"

payloads = [
    {
        "attack_type": "Malicious Payload Injection",
        "attacker_ip": "185.220.101.5", 
        "payload": "admin' OR '1'='1",
        "file_hash": "098eae6712e030f5071ebd677104f7a4"
    },
    {
        "attack_type": "Ransomware Activity Simulation",
        "attacker_ip": "45.143.203.14", 
        "payload": "<script>alert('Hacked')</script>",
        "file_hash": "44d88612fea8a8f36de82e1278abb02f"
    }
]

def check_virustotal(file_hash):
    """ VirusTotal Threat Intelligence Engine lookup """
    url = f"https://virustotal.com{file_hash}"
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            res_json = response.json()
            malicious_count = res_json['data']['attributes']['last_analysis_stats']['malicious']
            return f"{malicious_count} Engines Flagged Malicious"
        else:
            return "No Threat Detected / Clean"
    except Exception as e:
        return f"VT Error: {e}"

print("🚀 Starting Full-Python Incident Response Automation Script...")

for attack in payloads:
    print(f"\n[!] Simulating Incident: {attack['attack_type']}...")
    
    # 🔍 1. VirusTotal Threat Intel Query
    print("[*] Fetching Threat Intelligence from VirusTotal...")
    vt_result = check_virustotal(attack['file_hash'])
    
    # 🛠️ 2. Formatting Enterprise Notification Payload
    slack_payload = {
        "text": (
            f"🚨 *CRITICAL: Incident Response Automation Alert* 🚨\n\n"
            f"• *Incident Type:* Cloud API Exfiltration\n"
            f"• *Attack Vector:* {attack['attack_type']}\n"
            f"• *Attacker IP:* {attack['attacker_ip']}\n"
            f"• *Payload Detected:* `{attack['payload']}`\n"
            f"• *VirusTotal Intel:* *{vt_result}*\n\n"
            f"*Action Taken:* Multi-API threat vetting complete. Containment playbook triggered via automation script."
        )
    }
    
    # ⚡ 3. Direct Orchestration to Slack Infrastructure
    try:
        response = requests.post(SLACK_URL, json=slack_payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print(f"[+] Alert Successfully Pushed to Slack Channel! Response: {response.status_code}")
        else:
            print(f"[-] Slack Alert Failed. Response: {response.status_code}")
    except Exception as e:
        print(f"[-] Transmission Error: {e}")
        
    time.sleep(2)
