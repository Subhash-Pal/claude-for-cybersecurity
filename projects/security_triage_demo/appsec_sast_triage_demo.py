#!/usr/bin/env python3
"""
SAST Output Triage & False-Positive Filtering — Live Demo
============================================================
Session 5, Module 5.2 — AppSec Track
Claude for Cybersecurity — 60-Hour Curriculum

WHAT THIS DEMONSTRATES
-----------------------
A Semgrep scan against a sample codebase produced 12 findings. Some are real,
exploitable vulnerabilities; some are false positives (test fixtures, docs,
placeholder keys); some need human judgement. Claude triages the whole batch,
explains its reasoning per-finding, and produces a prioritized remediation
list — the noise-reduction step that normally takes an AppSec engineer
20-40 minutes per scan.

HOW TO RUN
----------
Demo mode (no API key needed, uses a pre-recorded realistic response):
    python3 appsec_sast_triage_demo.py

Live mode (calls the real Claude API):
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 appsec_sast_triage_demo.py --live

Requirements for --live mode:
    pip install anthropic
"""

import json
import os
import sys
import argparse
from pathlib import Path

VERDICT_ORDER = {"Confirmed": 0, "Needs Review": 1, "False Positive": 2}
VERDICT_COLOR = {
    "Confirmed": "\033[1;31m",       # bright red
    "Needs Review": "\033[0;33m",    # yellow
    "False Positive": "\033[0;32m",  # green
}
SEVERITY_COLOR = {
    "Critical": "\033[1;31m", "High": "\033[0;31m",
    "Medium": "\033[0;33m", "Low": "\033[0;36m", "N/A": "\033[0;37m",
}
RESET = "\033[0m"
BOLD = "\033[1m"

DATA_PATH = Path(__file__).parent / "sample_data" / "sast_findings.json"

SYSTEM_PROMPT = """You are a senior AppSec engineer triaging raw SAST scan output before it goes
into a sprint backlog. You will be given a list of Semgrep findings (rule, file, line, snippet, CWE).

For EACH finding, assign:
- verdict: one of "Confirmed" (real, exploitable issue), "Needs Review" (ambiguous, a human must
  check context), or "False Positive" (not actually exploitable given visible context — e.g. test
  fixtures, documentation placeholders, values that are clearly not real secrets)
- severity: Critical, High, Medium, Low, or N/A (use N/A only for False Positive verdicts)
- reasoning: one concise sentence justifying the verdict, referencing the actual code shown
- remediation: one concise, concrete fix, or "None needed" for false positives

Use the file path and snippet content as real signal — a finding in tests/ or docs/ with an
obvious placeholder value is very different from the same rule firing in production code with
user-controlled input reaching the sink.

Respond with ONLY a JSON array, no markdown fences, no preamble. Each element:
{"id": "...", "verdict": "...", "severity": "...", "reasoning": "...", "remediation": "..."}
"""

# Pre-recorded realistic response for demo mode.
MOCK_RESPONSE = [
    {"id": "SAST-001", "verdict": "Confirmed", "severity": "Critical", "reasoning": "customer_id is interpolated directly into a SQL string via an f-string with no parameterization, classic SQL injection.", "remediation": "Use a parameterized query: cursor.execute('SELECT * FROM invoices WHERE customer_id = %s', (customer_id,))."},
    {"id": "SAST-002", "verdict": "Confirmed", "severity": "Critical", "reasoning": "Using %s string formatting instead of parameterized execution still allows injection despite superficially resembling a placeholder.", "remediation": "Pass user_id as a bound parameter: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))."},
    {"id": "SAST-003", "verdict": "False Positive", "severity": "N/A", "reasoning": "This is a well-known publicly documented Stripe test-mode key (sk_test_...), explicitly commented as test mode only, and carries no production risk.", "remediation": "None needed; optionally move to a .env.example file to avoid repeated scanner noise."},
    {"id": "SAST-004", "verdict": "Confirmed", "severity": "High", "reasoning": "Flask debug mode bound to 0.0.0.0 exposes the interactive debugger and stack traces to the network if this reaches any non-local environment.", "remediation": "Set debug=False and drive it from an environment variable that defaults to False in production configs."},
    {"id": "SAST-005", "verdict": "Needs Review", "severity": "High", "reasoning": "eval() is used with a restricted __builtins__ dict, which reduces but does not eliminate sandbox-escape risk depending on what is in safe_vars.", "remediation": "Replace with a proper expression parser (e.g. asteval or a restricted-grammar formula library) rather than eval-based sandboxing."},
    {"id": "SAST-006", "verdict": "Confirmed", "severity": "Medium", "reasoning": "eval() on file contents from a local config file is lower risk than user input but still fragile and unnecessary; a malformed or tampered file causes arbitrary code execution.", "remediation": "Replace with json.load() or ast.literal_eval() for a config file that doesn't need arbitrary Python expressions."},
    {"id": "SAST-007", "verdict": "Confirmed", "severity": "High", "reasoning": "MD5 is used to hash a password, which is fast and unsalted-appearing here, making it highly vulnerable to offline cracking.", "remediation": "Replace with a password hashing function designed for this purpose, such as bcrypt, scrypt, or argon2."},
    {"id": "SAST-008", "verdict": "False Positive", "severity": "N/A", "reasoning": "MD5 is used here only to generate a cache ETag, a non-security integrity-of-caching use case, not a cryptographic security boundary.", "remediation": "None needed for security; MD5 is acceptable for non-adversarial cache-key generation."},
    {"id": "SAST-009", "verdict": "Confirmed", "severity": "High", "reasoning": "backup_name is interpolated into a shell=True command; if it can be influenced by any upstream input this is command injection.", "remediation": "Use subprocess.run(['tar', '-czf', f'{backup_name}.tar.gz', '/data']) with shell=False and a list of arguments."},
    {"id": "SAST-010", "verdict": "False Positive", "severity": "N/A", "reasoning": "This is a static, hardcoded string in a test fixture with no variable interpolation or external input, so shell=True carries no injection risk here.", "remediation": "None needed; optionally add a scanner suppression comment to reduce recurring noise on this fixture."},
    {"id": "SAST-011", "verdict": "Confirmed", "severity": "Critical", "reasoning": "mark_safe() disables autoescaping on what is described as user-supplied bio HTML, a direct stored-XSS vector.", "remediation": "Sanitize with a library such as bleach before marking safe, or avoid mark_safe and render as escaped text with limited allowed formatting."},
    {"id": "SAST-012", "verdict": "False Positive", "severity": "N/A", "reasoning": "This is a documentation quickstart example using the literal placeholder string 'YOUR_API_KEY_HERE', not a real credential.", "remediation": "None needed; this is expected content for a getting-started guide."},
]


def load_findings():
    with open(DATA_PATH) as f:
        return json.load(f)


def call_claude_live(findings):
    try:
        import anthropic
    except ImportError:
        sys.exit("Live mode requires the anthropic package: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Set ANTHROPIC_API_KEY in your environment to use --live mode.")

    client = anthropic.Anthropic(api_key=api_key)
    user_content = "Triage this SAST scan output:\n\n" + json.dumps(findings, indent=2)

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


def render_report(findings, triage):
    findings_by_id = {f["id"]: f for f in findings}
    triage_sorted = sorted(triage, key=lambda t: (VERDICT_ORDER.get(t["verdict"], 9)))

    print(f"\n{BOLD}{'='*82}{RESET}")
    print(f"{BOLD}  SAST TRIAGE REPORT — {len(findings)} raw Semgrep findings processed{RESET}")
    print(f"{BOLD}{'='*82}{RESET}\n")

    counts = {}
    for t in triage:
        counts[t["verdict"]] = counts.get(t["verdict"], 0) + 1
    summary = "  ".join(
        f"{VERDICT_COLOR.get(v, '')}{v}: {counts.get(v, 0)}{RESET}"
        for v in ["Confirmed", "Needs Review", "False Positive"]
        if counts.get(v, 0) > 0
    )
    noise_reduction = counts.get("False Positive", 0)
    print(f"  {summary}")
    print(f"  {BOLD}-> {noise_reduction} of {len(findings)} findings ({round(100*noise_reduction/len(findings))}%) "
          f"filtered out as noise before reaching the backlog{RESET}\n")

    for t in triage_sorted:
        finding = findings_by_id.get(t["id"], {})
        vcolor = VERDICT_COLOR.get(t["verdict"], "")
        scolor = SEVERITY_COLOR.get(t["severity"], "")

        print(f"  {vcolor}{BOLD}[{t['verdict'].upper():^15}]{RESET} {t['id']}  "
              f"{scolor}({t['severity']}){RESET}")
        print(f"      File:    {finding.get('file', 'unknown')}:{finding.get('line', '?')}")
        print(f"      Rule:    {finding.get('rule', 'unknown')}  ({finding.get('cwe', 'N/A')})")
        print(f"      Why:     {t['reasoning']}")
        print(f"      Fix:     {BOLD}{t['remediation']}{RESET}")
        print()

    print(f"{BOLD}{'-'*82}{RESET}")
    confirmed_critical = [t for t in triage if t["verdict"] == "Confirmed" and t["severity"] == "Critical"]
    if confirmed_critical:
        print(f"  {VERDICT_COLOR['Confirmed']}{BOLD}SHIP-BLOCKING{RESET}: "
              f"{len(confirmed_critical)} Critical confirmed findings should block this release: "
              f"{', '.join(t['id'] for t in confirmed_critical)}")
    print(f"{BOLD}{'-'*82}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="AppSec SAST Triage demo")
    parser.add_argument("--live", action="store_true", help="Call the real Claude API instead of using the demo response")
    args = parser.parse_args()

    findings = load_findings()

    print(f"\nLoaded {len(findings)} raw Semgrep findings from sample_data/sast_findings.json")

    if args.live:
        print("\nCalling Claude API (live mode)...")
        triage = call_claude_live(findings)
    else:
        print("\nRunning in DEMO mode (pre-recorded response, no API key needed).")
        print("Use --live with ANTHROPIC_API_KEY set to call the real API.")
        triage = MOCK_RESPONSE

    render_report(findings, triage)


if __name__ == "__main__":
    main()
