#!/usr/bin/env python3
"""
SOC Alert Triage & Severity Scoring — Live Demo
=================================================
Session 3, Module 3.2 — SOC/SecOps Track
Claude for Cybersecurity — 60-Hour Curriculum

WHAT THIS DEMONSTRATES
-----------------------
A SOC analyst is handed a raw queue of 15 alerts from EDR, firewall, IDS,
DLP, AD, cloud, and SaaS monitoring tools. Claude triages the whole queue
in one pass: assigns severity, flags likely-related alerts (same asset,
escalating pattern), and produces a ranked action list — the kind of
first-pass triage that normally eats 20-30 minutes of an analyst's shift.

HOW TO RUN
----------
Demo mode (no API key needed, uses a pre-recorded realistic response):
    python3 soc_alert_triage_demo.py

Live mode (calls the real Claude API):
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 soc_alert_triage_demo.py --live

Requirements for --live mode:
    pip install anthropic
"""

import json
import os
import sys
import argparse
from pathlib import Path

SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}
SEVERITY_COLOR = {
    "Critical": "\033[1;31m",   # bright red
    "High": "\033[0;31m",       # red
    "Medium": "\033[0;33m",     # yellow
    "Low": "\033[0;36m",        # cyan
    "Informational": "\033[0;37m",  # grey
}
RESET = "\033[0m"
BOLD = "\033[1m"

DATA_PATH = Path(__file__).parent / "sample_data" / "alerts.json"

SYSTEM_PROMPT = """You are a senior SOC analyst assistant. You will be given a raw queue of
security alerts from multiple sources (EDR, firewall, IDS, DLP, AD, cloud, SaaS monitoring).

For EACH alert, assign:
- severity: one of Critical, High, Medium, Low, Informational
- confidence: your confidence in this assessment as a percentage
- related_to: a list of other alert IDs that appear to be part of the same incident
  (same asset, escalating pattern, temporal proximity), or an empty list
- reasoning: one concise sentence explaining the severity assignment
- recommended_action: one concise, concrete next step for the analyst

Look actively for attack chains: a single low-severity alert can become Critical when
correlated with others on the same asset within a short time window. Prioritize catching
these chains over scoring each alert in isolation.

Respond with ONLY a JSON array, no markdown fences, no preamble. Each element:
{"id": "...", "severity": "...", "confidence": 0-100, "related_to": ["..."], "reasoning": "...", "recommended_action": "..."}
"""

# Pre-recorded realistic response for demo mode — mirrors what Claude actually
# returns for this exact alert set, so the demo runs identically offline.
MOCK_RESPONSE = [
    {"id": "ALT-1001", "severity": "High", "confidence": 80, "related_to": ["ALT-1003", "ALT-1004", "ALT-1010", "ALT-1011", "ALT-1015"], "reasoning": "Encoded PowerShell spawned from Word is a classic initial-access pattern and this asset is central to a larger chain.", "recommended_action": "Isolate FIN-WKS-0042 from the network immediately and begin forensic triage."},
    {"id": "ALT-1002", "severity": "Low", "confidence": 70, "related_to": [], "reasoning": "Routine internet background-noise port scan against DMZ, no follow-on activity observed.", "recommended_action": "Log and monitor; no immediate action required."},
    {"id": "ALT-1003", "severity": "Critical", "confidence": 90, "related_to": ["ALT-1001", "ALT-1004", "ALT-1010", "ALT-1011", "ALT-1015"], "reasoning": "Persistence mechanism (scheduled task re-launching a temp-folder binary) on an already-suspicious host.", "recommended_action": "Preserve the scheduled task and binary for forensics, then remove persistence after isolation."},
    {"id": "ALT-1004", "severity": "Critical", "confidence": 88, "related_to": ["ALT-1001", "ALT-1003", "ALT-1011", "ALT-1015"], "reasoning": "Large outbound transfer to an unrecognized domain immediately after persistence was established strongly suggests data exfiltration.", "recommended_action": "Block the destination domain at the firewall/proxy and identify what data left the host."},
    {"id": "ALT-1005", "severity": "Low", "confidence": 75, "related_to": [], "reasoning": "Single blocked SQLi attempt with WAF returning 403; no evidence of success.", "recommended_action": "No action beyond routine logging; monitor source IP for repeat attempts."},
    {"id": "ALT-1006", "severity": "Critical", "confidence": 92, "related_to": ["ALT-1001", "ALT-1003", "ALT-1004", "ALT-1010", "ALT-1011", "ALT-1015"], "reasoning": "Service account authentication failures followed by success, originating from the already-compromised finance workstation, indicates credential compromise in progress.", "recommended_action": "Force-reset svc-backup credentials immediately and review all recent authentications from this account."},
    {"id": "ALT-1007", "severity": "Informational", "confidence": 85, "related_to": [], "reasoning": "Adware was auto-quarantined by EDR; no further exposure.", "recommended_action": "No action needed; confirm quarantine succeeded."},
    {"id": "ALT-1008", "severity": "High", "confidence": 82, "related_to": [], "reasoning": "Backup bucket made publicly readable is a direct data-exposure risk regardless of intent.", "recommended_action": "Revert the ACL to private immediately and audit whether the bucket was accessed while public."},
    {"id": "ALT-1009", "severity": "Medium", "confidence": 70, "related_to": [], "reasoning": "Credential-harvesting link was clicked but this appears unrelated to the finance-workstation chain based on asset and timing.", "recommended_action": "Force password reset for r.iyer and check for suspicious mailbox activity."},
    {"id": "ALT-1010", "severity": "Critical", "confidence": 90, "related_to": ["ALT-1001", "ALT-1003", "ALT-1004", "ALT-1006", "ALT-1011", "ALT-1015"], "reasoning": "Direct attempt to read LSASS memory is credential dumping behavior, blocked but confirms active intrusion.", "recommended_action": "Treat as confirmed active intrusion; escalate to Tier 3 / incident commander now."},
    {"id": "ALT-1011", "severity": "Critical", "confidence": 93, "related_to": ["ALT-1001", "ALT-1003", "ALT-1004", "ALT-1006", "ALT-1010", "ALT-1015"], "reasoning": "Outbound connection to an IP matching a fresh threat-intel C2 entry, from the same host as the rest of the chain, confirms command-and-control.", "recommended_action": "Block the C2 IP network-wide immediately and treat as a confirmed active breach."},
    {"id": "ALT-1012", "severity": "Medium", "confidence": 60, "related_to": [], "reasoning": "Off-hours bulk export is anomalous but could be legitimate; needs owner verification.", "recommended_action": "Contact the sales manager directly to verify the export was authorized."},
    {"id": "ALT-1013", "severity": "Low", "confidence": 78, "related_to": [], "reasoning": "Automated CMS-path scanning with all 404 responses; no successful access.", "recommended_action": "Log and monitor; consider rate-limiting or blocking the source IP if it persists."},
    {"id": "ALT-1014", "severity": "Medium", "confidence": 55, "related_to": [], "reasoning": "Unsigned driver correlates with a same-day GPU tool install, likely legitimate but violates driver-signing policy.", "recommended_action": "Verify the driver against the installed utility and remove if unauthorized; low urgency."},
    {"id": "ALT-1015", "severity": "Critical", "confidence": 95, "related_to": ["ALT-1001", "ALT-1003", "ALT-1004", "ALT-1006", "ALT-1010", "ALT-1011"], "reasoning": "Domain Admin group membership was granted to the just-compromised service account 90 minutes into an active intrusion chain — this is privilege escalation to full domain control.", "recommended_action": "Immediately revoke the Domain Admin grant, disable svc-backup and jsharma pending investigation, and activate the incident response plan."},
]


def load_alerts():
    with open(DATA_PATH) as f:
        return json.load(f)


def call_claude_live(alerts):
    try:
        import anthropic
    except ImportError:
        sys.exit("Live mode requires the anthropic package: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Set ANTHROPIC_API_KEY in your environment to use --live mode.")

    client = anthropic.Anthropic(api_key=api_key)
    user_content = "Triage this alert queue:\n\n" + json.dumps(alerts, indent=2)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )

    text = "".join(block.text for block in response.content if block.type == "text")
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def render_report(alerts, triage):
    alerts_by_id = {a["id"]: a for a in alerts}
    triage_sorted = sorted(triage, key=lambda t: SEVERITY_ORDER.get(t["severity"], 9))

    print(f"\n{BOLD}{'='*78}{RESET}")
    print(f"{BOLD}  SOC ALERT TRIAGE REPORT — {len(alerts)} alerts processed{RESET}")
    print(f"{BOLD}{'='*78}{RESET}\n")

    counts = {}
    for t in triage:
        counts[t["severity"]] = counts.get(t["severity"], 0) + 1
    summary = "  ".join(
        f"{SEVERITY_COLOR.get(sev, '')}{sev}: {counts.get(sev, 0)}{RESET}"
        for sev in ["Critical", "High", "Medium", "Low", "Informational"]
        if counts.get(sev, 0) > 0
    )
    print(f"  {summary}\n")

    seen_chains = set()
    for t in triage_sorted:
        alert = alerts_by_id.get(t["id"], {})
        color = SEVERITY_COLOR.get(t["severity"], "")
        chain_tag = ""
        if t["related_to"]:
            chain_key = tuple(sorted([t["id"]] + t["related_to"]))
            if chain_key not in seen_chains:
                seen_chains.add(chain_key)
            chain_tag = f"  {BOLD}[CHAIN: {len(t['related_to'])+1} related alerts]{RESET}"

        print(f"  {color}{BOLD}[{t['severity'].upper():^13}]{RESET} {t['id']}  "
              f"({t.get('confidence','?')}% confidence){chain_tag}")
        print(f"      Asset:   {alert.get('asset', 'unknown')}")
        print(f"      Type:    {alert.get('alert_type', 'unknown')}")
        print(f"      Why:     {t['reasoning']}")
        print(f"      Action:  {BOLD}{t['recommended_action']}{RESET}")
        print()

    critical_chain = [t for t in triage if t["severity"] == "Critical" and t["related_to"]]
    if critical_chain:
        chain_ids = sorted(set([t["id"] for t in critical_chain] +
                                [rid for t in critical_chain for rid in t["related_to"]]))
        print(f"{BOLD}{'-'*78}{RESET}")
        print(f"  {SEVERITY_COLOR['Critical']}{BOLD}ATTACK CHAIN DETECTED{RESET} across {len(chain_ids)} alerts: "
              f"{', '.join(chain_ids)}")
        print(f"  Raw queue gave no indication these were connected — grouped only after triage.")
        print(f"{BOLD}{'-'*78}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="SOC Alert Triage demo")
    parser.add_argument("--live", action="store_true", help="Call the real Claude API instead of using the demo response")
    args = parser.parse_args()

    alerts = load_alerts()

    print(f"\nLoaded {len(alerts)} raw alerts from sample_data/alerts.json")
    print("(sources: EDR, Firewall, IDS, DLP, AD, Cloud, SaaS Monitor)")

    if args.live:
        print("\nCalling Claude API (live mode)...")
        triage = call_claude_live(alerts)
    else:
        print("\nRunning in DEMO mode (pre-recorded response, no API key needed).")
        print("Use --live with ANTHROPIC_API_KEY set to call the real API.")
        triage = MOCK_RESPONSE

    render_report(alerts, triage)


if __name__ == "__main__":
    main()
