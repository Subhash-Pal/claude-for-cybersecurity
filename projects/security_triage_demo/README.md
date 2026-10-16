# Claude for Cybersecurity — Live Demo Package

Two working demos from the 60-hour curriculum, each in two formats:

| Track | Session/Module | Python (terminal) | Browser (interactive) |
|---|---|---|---|
| SOC/SecOps | 3.2 — Alert Triage & Severity Scoring | `soc_alert_triage_demo.py` | `security_triage_demo.html` (SOC tab) |
| AppSec | 5.2 — SAST Output Triage | `appsec_sast_triage_demo.py` | `security_triage_demo.html` (AppSec tab) |

## Quick start — terminal demos

No setup, no API key required. Both scripts ship with a pre-recorded realistic
Claude response so they run identically offline — useful for a live demo where
you don't want to depend on venue wifi.

```bash
python3 soc_alert_triage_demo.py
python3 appsec_sast_triage_demo.py
```

To call the real API instead:

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python3 soc_alert_triage_demo.py --live
python3 appsec_sast_triage_demo.py --live
```

## Quick start — browser demo

`security_triage_demo.html` is a self-contained interactive demo with tabs for
both tracks. It calls the live Claude API directly from the browser, so it
always needs a working connection — use it when you want the "click a button,
watch it reason live" moment in front of an audience.

- **If opened as a Claude.ai Artifact:** the API call is proxied automatically,
  no key needed — just open the file as an artifact and click "Run Claude Triage."
- **If opened as a standalone HTML file outside Claude.ai:** the fetch call to
  `api.anthropic.com` will need a key attached (e.g. via a small local proxy,
  since browsers can't safely hold a raw API key). For a live client demo,
  running it as a Claude.ai artifact is the simplest path — no proxy needed.

## What each demo shows

**SOC Alert Triage** — 15 synthetic alerts (EDR, firewall, IDS, DLP, AD, cloud,
SaaS) are fed to Claude as a raw, unsorted queue exactly as a SOC analyst would
receive them. Claude assigns severity, confidence, and — the key moment — flags
that six individually-plausible alerts actually form a single attack chain
(initial access → persistence → exfiltration → credential dumping → C2 → domain
admin escalation) that the raw queue gives no indication of.

**AppSec SAST Triage** — 12 synthetic Semgrep findings mix real vulnerabilities
(SQL injection, hardcoded MD5 password hashing, shell injection, stored XSS)
with false positives (test fixtures, documentation placeholders, non-security
MD5 usage). Claude triages each with file/line reasoning and produces a
ship-blocking summary — the noise-reduction step AppSec engineers do manually
after every scan.

## Files

```
soc_alert_triage_demo.py       — SOC terminal demo
appsec_sast_triage_demo.py     — AppSec terminal demo
security_triage_demo.html      — combined interactive browser demo
sample_data/alerts.json        — 15 synthetic SOC alerts
sample_data/sast_findings.json — 12 synthetic Semgrep findings
requirements.txt               — Python dependencies for --live mode
```

All data is synthetic — no real logs, credentials, or production code. Safe to
run and show without any data-handling concerns, which also doubles as a live
example of the Session 2 governance principle (don't paste real security data
into a prompt without knowing why).

## Customizing for a specific client demo

Swap `sample_data/alerts.json` or `sample_data/sast_findings.json` for data
shaped like the client's actual environment (still synthetic — same fields,
different asset names / tech stack) to make the demo feel native to their
context rather than generic.
