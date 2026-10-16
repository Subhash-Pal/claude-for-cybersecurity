# Claude for Cybersecurity — Live Demo Package

> **Part of [Claude for Cybersecurity](https://github.com/Subhash-Pal/claude-for-cybersecurity/blob/main/docs/Claude_Security_60hr_Detailed_Course_Outline.md)**, a 60-hour hands-on curriculum on applying Claude to security work. This is the first runnable project in the series.

## Purpose & context

Security teams don't lack data, they lack time to read it. A SOC analyst faces hundreds of alerts per shift, and an AppSec engineer faces thousands of scanner findings per release. Most of it is noise, and the few items that matter are easy to miss because they look harmless on their own.

This module demonstrates the first and most practical use of Claude in security: **triage**. That means taking a raw, unsorted pile of machine-generated output and turning it into a prioritized, explained, decision-ready list that a human can act on.

It covers two tracks of the curriculum, using the same pattern:

| Track | Problem | What Claude does |
|---|---|---|
| **SOC / SecOps** (Session 3.2) | A flat queue of alerts from many tools, with no sense of which ones are connected | Scores severity and confidence, then correlates alerts into a single attack chain |
| **AppSec** (Session 5.2) | A scanner report where real vulnerabilities are buried among false positives | Judges each finding in its file and line context and separates true issues from noise |

### How it works

Both demos follow the same pipeline:

1. **Load** synthetic input from `sample_data/` (alerts or SAST findings, as JSON).
2. **Prompt** Claude with the raw data and a clear triage task (role, criteria, required output structure).
3. **Reason**: Claude assigns severity and confidence, explains each judgment, and looks for relationships across items.
4. **Report**: the result is rendered as a prioritized summary (terminal output or an interactive browser view).

Each terminal script can run in two modes. The default replays a pre-recorded Claude response so the demo works offline and behaves identically every time. `--live` sends the data to the real API.

### Design principles

- **Human in the loop.** Claude recommends and explains. The analyst or engineer makes the final call.
- **Synthetic data only.** Nothing here comes from a real environment, so it is safe to run, share and show.
- **Reproducible.** The offline mode removes the dependency on network and API availability, which makes it reliable for live demos and teaching.
- **Explainable output.** Every verdict comes with its reasoning, so the output can be checked rather than blindly trusted.

### What you should take away

- Why correlating alerts matters more than scoring them one at a time (the attack chain moment).
- How added context (file path, line, code intent) separates real findings from false positives.
- How to structure a triage prompt and what output format makes it usable.
- Where an LLM helps in the triage loop and where a human must still decide.

### How this fits the series

This project is the foundation for later modules. The triage pattern of raw data, structured prompt, reasoned output and human decision extends to threat intel enrichment, incident response and detection engineering. Each of those will be added as its own folder under `projects/` in the root repository.

---

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
README.md                      — this file
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
