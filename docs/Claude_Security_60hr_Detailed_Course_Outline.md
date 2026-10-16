# Claude for Cybersecurity — 60-Hour Role-Differentiated Curriculum
## Detailed Course Outline

**Format:** 14 sessions across 7 tracks (2 sessions per specialist track, 2 shared Foundation sessions)
**Base:** Redesigned from Vinsys 32-Hour Training Plan per gap analysis
**Delivery:** Instructor-led, ~40% lecture / 60% hands-on lab per session

---

## Executive Summary

This 60-hour curriculum replaces a single linear track with role-differentiated paths across seven cybersecurity disciplines. Every participant completes the two-session Foundation block; specialist sessions can then run as parallel tracks for mixed-role cohorts, or sequentially for single-discipline teams. Secure AI Usage and Automation are cross-cutting and recommended for all personas regardless of primary track.

### Overall Learning Outcomes
By the end of the program, participants will be able to:
- Apply Claude correctly within their specific security role, with an accurate model of its limitations and reliability boundaries.
- Execute role-specific workflows: alert triage (SOC), secure code review (AppSec), misconfiguration analysis (Cloud), control mapping (GRC), IOC/ATT&CK mapping (Threat Intel).
- Build and defend against prompt injection, and apply verification workflows appropriate to their decision-criticality.
- Integrate Claude into existing tooling — SIEM, SAST, ticketing, CI/CD, Kubernetes — via API and MCP.
- Draft governance documentation for responsible AI use in security operations, including DPDP Act alignment.

---

## SESSION 1: Claude & Security Fundamentals (Foundation I — 4.5 hrs)
*All participants*

### Module 1.1 — Understanding Claude & LLMs in Security Contexts (1.0 hr)
**Key Topics**
- What LLMs are and how Claude generates responses; parallels to threat modeling reasoning
- Claude model family: speed vs. reasoning depth trade-offs for security operations
- Tokens and context windows: managing large security datasets (logs, vulnerability reports)
- Knowledge cutoffs: why Claude is not a real-time threat intelligence platform
- Hallucination risk in security-critical decisions

**Hands-On Lab:** Review five security-focused prompt/response pairs (incident alerts, CVE descriptions, policy text). Classify each response as decision-safe or requiring verification; document the reasoning.

### Module 1.2 — Claude Interface & Security-Focused Features (1.0 hr)
**Key Topics**
- Chat interface for investigations; Projects for organizing threat models and post-mortems
- File uploads: processing logs, policies, vulnerability reports
- Web search for CVE verification and emerging threat intel
- Data retention, privacy settings, and enterprise configuration

**Hands-On Lab:** Create a Project for "Incident Response Lab," upload a sanitized synthetic log file, and generate a structured anomaly summary.

### Module 1.3 — Security-Focused Prompt Engineering Fundamentals (1.5 hrs)
**Key Topics**
- Anatomy of a strong security prompt: context, scope, output format, constraints
- Role-based prompting ("assume you are a senior threat analyst") for expert-level reasoning
- Few-shot prompting using prior assessments as examples
- Structured output: JSON for automation, severity ratings, actionable remediation
- Common pitfalls: vague threats, missing context, over-reliance for critical decisions

**Hands-On Lab:** Rewrite three weak prompts ("Is this malware?", "Analyze the attack", "Check this code") into precise, structured requests. Compare output quality before/after.

### Module 1.4 — Real-World Security Use Cases Overview (1.0 hr)
**Key Topics**
- Cross-role preview: log analysis, threat intel synthesis, IR drafting, policy work, risk assessment, architecture review
- How the same core skills apply differently across SOC, AppSec, Cloud, GRC, and Threat Intel roles

**Hands-On Lab:** Complete one end-to-end mini-task (analyze a synthetic security alert, extract key details, draft a two-paragraph preliminary summary) as a baseline skill check before track specialization begins.

---

## SESSION 2: Responsible Use, Governance & Prompting Mastery (Foundation II — 4.5 hrs)
*All participants*

### Module 2.1 — Responsible & Secure Use of Claude (1.5 hrs)
**Key Topics**
- Data confidentiality: what security data is/isn't appropriate to share (PII, credentials, exploit code)
- Recognizing hallucinations: verification workflows and confidence scoring
- Bias and limitations in threat modeling and risk scoring
- Keeping humans in the loop: tool vs. decision-maker boundary

**Hands-On Lab:** Review 12 security scenarios; classify each as safe-for-Claude, needs-verification, or do-not-use. Justify each classification.

### Module 2.2 — Data Confidentiality & Governance in Security Contexts (1.0 hr)
**Key Topics**
- Organizational data handling policy design for AI tool use
- Retention and compliance considerations (including DPDP Act basics for Indian enterprise context)
- Approval workflows and audit trails for AI-assisted security work

**Hands-On Lab:** Draft a one-page "acceptable use" guideline for Claude in a security team, covering what can and cannot be pasted into a prompt.

### Module 2.3 — Advanced Prompting Techniques (2.0 hrs)
**Key Topics**
- Chain-of-thought prompting for multi-stage security reasoning
- Structured reasoning frameworks: MITRE ATT&CK, risk matrices, attack trees (introduced here, applied in depth in Session 12)
- Prompt decomposition: breaking large investigations into chainable sub-tasks
- Building reusable, team-shareable prompt templates

**Hands-On Lab:** Design a reusable prompt template for a recurring task in the participant's own role; test with sample data and refine through two iterations.

---

## SESSION 3: Alert Triage & SIEM Analysis (SOC/SecOps I — 5.0 hrs)

### Module 3.1 — SOC Workflows & Where Claude Fits (1.0 hr)
**Key Topics**
- SOC tiering (Tier 1/2/3) and where AI assistance adds the most value at each tier
- MTTD/MTTR framing and how Claude-assisted triage affects both
- Boundaries: what a human analyst must always confirm before action

### Module 3.2 — Alert Triage & Severity Scoring (1.5 hrs)
**Key Topics**
- Building a consistent severity/urgency rubric for prompt-based triage
- Reducing alert fatigue: batch summarization of low-fidelity alerts
- Distinguishing true positive indicators from noise using structured prompts

**Hands-On Lab:** Given a synthetic queue of 15–20 alerts, use Claude to triage, score, and rank by urgency. Compare against an answer key; measure agreement rate.

### Module 3.3 — SIEM Log Analysis & IOC Extraction (1.5 hrs)
**Key Topics**
- Parsing and summarizing large log exports (Splunk/Sentinel/Elastic-style formats)
- Extracting IOCs (IPs, hashes, domains) into structured output
- Pattern identification across multi-source logs

**Hands-On Lab:** Process a synthetic SIEM export with planted anomalies; extract IOCs into a structured JSON report suitable for downstream tooling.

### Module 3.4 — Alert Enrichment with Threat Context (1.0 hr)
**Key Topics**
- Enriching raw alerts with CVE/threat-intel context
- Correlating alert patterns against known attack techniques (preview of ATT&CK mapping)

**Hands-On Lab:** Take three raw alerts and enrich each with likely technique, plausible attacker goal, and recommended next investigative step.

---

## SESSION 4: Threat Hunting & IR Automation (SOC/SecOps II — 5.0 hrs)

### Module 4.1 — Hypothesis-Driven Threat Hunting (1.5 hrs)
**Key Topics**
- Formulating hunt hypotheses from threat intel and anomaly patterns
- Using Claude to generate hunt queries and reasoning chains
- Evaluating hunt results and iterating on hypotheses

**Hands-On Lab:** Given a threat intel brief, formulate two hunt hypotheses and draft corresponding hunt queries with Claude's assistance.

### Module 4.2 — Incident Response Timeline & Root Cause Drafting (1.5 hrs)
**Key Topics**
- Drafting IR timelines from fragmented log/alert evidence
- Root cause analysis structuring
- Post-mortem documentation best practices

**Hands-On Lab:** Complete an incident response task end-to-end: analyze a synthetic security alert, extract key details, draft a preliminary incident report with timeline and recommended actions.

### Module 4.3 — Escalation Workflows & Tier Handoff (1.0 hr)
**Key Topics**
- Designing clear escalation criteria (Tier 1 → Tier 2 → Tier 3)
- Documenting findings for human review at each handoff point
- When Claude's confidence should trigger automatic escalation

**Hands-On Lab:** Design an escalation decision tree for a recurring alert type; test it against five scenarios.

### Module 4.4 — IR Automation Pipeline Design (1.0 hr)
**Key Topics**
- Detect anomaly → enrichment → Claude analysis → escalation pipeline pattern
- Orchestration options (preview — full build in Session 14)

**Hands-On Lab:** Map an IR automation pipeline for the participant's own environment; document data flow and human checkpoints.

---

## SESSION 5: Secure Code Review & SAST Triage (AppSec I — 3.5 hrs)

### Module 5.1 — Code Explanation & Vulnerability Pattern Identification (1.0 hr)
**Key Topics**
- Explaining unfamiliar code and libraries
- Identifying common vulnerability patterns: SQLi, XSS, CSRF, buffer overflows, XXE

**Hands-On Lab:** Analyze a multi-file code sample with intentional vulnerabilities; identify and explain each by severity.

### Module 5.2 — SAST Output Triage & False-Positive Filtering (1.5 hrs)
**Key Topics**
- Reducing SAST tool noise (Semgrep/SonarQube/Checkmarx-style output)
- Deduplication and false-positive filtering with structured prompts
- Prioritizing findings by exploitability and business impact

**Hands-On Lab:** Given a synthetic SAST scan output (from an OSS vulnerable-by-design app such as Juice Shop or DVWA), triage findings into confirmed/needs-review/false-positive buckets.

### Module 5.3 — Cryptographic & Supply Chain Review (1.0 hr)
**Key Topics**
- Analyzing cryptographic implementations: weak algorithms, key management flaws
- Supply chain risk assessment: dependency evaluation, package trustworthiness

**Hands-On Lab:** Review a dependency manifest for known-risky packages and outdated cryptographic library usage; produce a short risk memo.

---

## SESSION 6: Vulnerability Remediation & Secure Coding (AppSec II — 3.5 hrs)

### Module 6.1 — Secure Code Generation & Hardening (1.5 hrs)
**Key Topics**
- Generating secure code templates: authentication, input validation, logging
- Building defense-in-depth: layered validation and controls
- Common pitfalls: over-trusting generated code, missed edge cases

**Hands-On Lab:** Request a secure Python script for log parsing and validation with threat detection built in; review, refine, and test the output.

### Module 6.2 — Structured Vulnerability Remediation Workflow (1.0 hr)
**Key Topics**
- Turning a vulnerability finding into a remediation plan with clear acceptance criteria
- Writing security advisories from code analysis findings

**Hands-On Lab:** Take three findings from Session 5's SAST triage and draft remediation plans plus advisory text for each.

### Module 6.3 — Secure SDLC Gates & PR-Blocking Checks (1.0 hr)
**Key Topics**
- Designing pre-commit and PR-blocking checks using Claude-assisted review
- Where automated gates should defer to human review

**Hands-On Lab:** Design a PR review checklist that incorporates a Claude-assisted security check step; define pass/fail/escalate criteria.

---

## SESSION 7: IAM & Misconfiguration Analysis — Azure (Cloud Security I — 5.0 hrs)

### Module 7.1 — Cloud Security Fundamentals & Claude's Role (1.0 hr)
**Key Topics**
- Shared responsibility model and where AI-assisted analysis fits
- Cloud-specific hallucination risks (invented service names, deprecated API calls)

### Module 7.2 — IAM Policy Analysis & Least-Privilege Review (1.5 hrs)
**Key Topics**
- Reading and explaining IAM policy JSON/role definitions
- Identifying over-privileged roles and privilege escalation paths
- Recommending least-privilege corrections

**Hands-On Lab:** Given exported Azure IAM role definitions (sandbox tenant or sample JSON), identify over-privileged assignments and draft corrected policies.

### Module 7.3 — Misconfiguration Detection, CSPM-Style (1.5 hrs)
**Key Topics**
- Common misconfiguration classes: public storage, open network security groups, disabled logging
- Structuring prompts to scan configuration exports systematically

**Hands-On Lab:** Review a set of synthetic Azure resource configurations; flag misconfigurations and prioritize by exposure risk.

### Module 7.4 — Azure Security Services Integration (1.0 hr)
**Key Topics**
- Connecting Claude to Azure Security Center / Defender findings
- Contextualizing alerts with Azure-specific threat intelligence

**Hands-On Lab:** Draft an integration design mapping Azure Defender alert output through Claude analysis to a remediation ticket.

---

## SESSION 8: Kubernetes & Container Security (Cloud Security II — 5.0 hrs)

### Module 8.1 — Container Image Hardening (1.5 hrs)
**Key Topics**
- Dockerfile review for common hardening gaps (root user, unpinned base images, exposed secrets)
- Image scanning output interpretation

**Hands-On Lab:** Review a set of sample Dockerfiles with intentional issues; produce hardened versions.

### Module 8.2 — Kubernetes Manifest Security Review (1.5 hrs)
**Key Topics**
- Reviewing pod security contexts, network policies, RBAC bindings
- Identifying privilege escalation paths in manifest configuration

**Hands-On Lab:** Given sample K8s manifests (deployable to a local kind/minikube cluster), identify security gaps and correct them.

### Module 8.3 — Runtime Behavior & Admission Control (1.0 hr)
**Key Topics**
- Interpreting runtime security tool output (e.g., Falco-style alerts)
- Designing admission control policies with Claude assistance

**Hands-On Lab:** Draft an admission control policy that would have blocked the misconfigurations identified in Module 8.2.

### Module 8.4 — Cloud Security Capstone (1.0 hr)
**Key Topics**
- End-to-end cloud security review: IAM + misconfiguration + container/K8s findings combined
- Prioritization and remediation roadmap creation

**Hands-On Lab:** Produce a consolidated cloud security findings report across all Session 7–8 labs, prioritized by exploitability.

---

## SESSION 9: Policy Drafting & Control Mapping (GRC/Compliance I — 3.5 hrs)

### Module 9.1 — Security Policy Drafting with Claude (1.5 hrs)
**Key Topics**
- Drafting security policies from requirements and regulatory input
- Gap analysis: comparing existing policy against a target framework

**Hands-On Lab:** Draft a data-handling policy section from a set of stated requirements; compare against a reference control.

### Module 9.2 — Control Framework Mapping (1.5–2.0 hrs)
**Key Topics**
- Mapping organizational controls to NIST 800-53 / ISO 27001 Annex A structures
- India-specific alignment: DPDP Act requirements and how they map to existing control families
- Identifying control gaps and drafting remediation narratives

**Hands-On Lab:** Given a partial control set, map each control to its corresponding NIST/ISO reference and flag DPDP-relevant gaps.

---

## SESSION 10: Audit Evidence, Risk & DPDP (GRC/Compliance II — 3.5 hrs)

### Module 10.1 — Audit Evidence Generation (1.0 hr)
**Key Topics**
- Structuring audit evidence packages from raw operational data
- Drafting evidence narratives that satisfy auditor requests without over-disclosure

**Hands-On Lab:** Given a sample audit request list, draft evidence summaries for three requested controls.

### Module 10.2 — Risk Register & Risk Scoring (1.5 hrs)
**Key Topics**
- Structuring a risk register: likelihood, impact, treatment
- Using Claude to draft risk narratives and prioritize the register

**Hands-On Lab:** Build a risk register from five identified findings (drawn from earlier AppSec/Cloud sessions), scored and prioritized.

### Module 10.3 — DPDP Act Compliance Documentation (1.0 hr)
**Key Topics**
- Core DPDP Act obligations relevant to security/data-handling teams
- Drafting DPDP-aligned data processing records and breach notification templates

**Hands-On Lab:** Draft a DPDP-aligned breach notification template using a synthetic incident scenario as input.

---

## SESSION 11: CVE & IOC Analysis (Threat Intelligence I — 4.0 hrs)

### Module 11.1 — CVE Analysis & Exploitability Assessment (1.5 hrs)
**Key Topics**
- Interpreting CVE/NVD data: CVSS scoring, affected versions, exploit maturity
- Assessing real-world exploitability beyond the raw score

**Hands-On Lab:** Given a vulnerability report for an open-source library, use Claude (optionally with NVD API access) to assess exploitability, affected versions, and recommend patches or workarounds.

### Module 11.2 — IOC Extraction & Enrichment (1.5 hrs)
**Key Topics**
- Structured IOC extraction from threat reports and logs
- Enriching IOCs with contextual threat intelligence

**Hands-On Lab:** Extract and enrich IOCs from a sample threat intelligence report into a structured, shareable format.

### Module 11.3 — Threat Actor Profiling Basics (1.0 hr)
**Key Topics**
- Synthesizing actor TTP patterns from multiple reports
- Building a lightweight actor profile from available intelligence

**Hands-On Lab:** Given three synthetic threat reports referencing the same actor, synthesize a one-page profile.

---

## SESSION 12: MITRE ATT&CK Mapping & RAG for Threat Intel (Threat Intelligence II — 4.0 hrs)

### Module 12.1 — MITRE ATT&CK Technique Mapping (1.5 hrs)
**Key Topics**
- Mapping observed behaviors to ATT&CK tactics and techniques
- Using the ATT&CK Navigator alongside Claude-assisted mapping

**Hands-On Lab:** Map a synthetic attack scenario's observed behaviors to specific ATT&CK techniques using the Navigator and Claude jointly; document the mapping rationale.

### Module 12.2 — RAG for Private Threat Intelligence (2.0 hrs)
**Key Topics**
- Why RAG reduces hallucination when grounding Claude in proprietary threat data
- Chunking and indexing threat intel documents; retrieval pipeline design
- Evaluating RAG output quality: traceability and relevance

**Hands-On Lab:** Build a minimal Q&A system over a small set of private threat intel documents — chunk, embed (local FAISS/Chroma), retrieve, and ground Claude's answers in the retrieved context.

### Module 12.3 — Threat Intelligence Capstone (0.5 hr)
**Key Topics**
- Combining CVE/IOC/ATT&CK/RAG skills into a single analyst workflow

**Hands-On Lab:** Given a new synthetic incident, produce a combined threat intelligence brief using techniques from both Session 11 and 12.

---

## SESSION 13: Guardrails, Privacy & Prompt Injection Defense (Secure AI Usage — 5.0 hrs)
*Recommended for all roles*

### Module 13.1 — Data Confidentiality Deep Dive (1.0 hr)
**Key Topics**
- Detailed treatment of what security data categories are/aren't safe to share
- Handling credentials, exploit code, and PII in prompts

**Hands-On Lab:** Audit five real (redacted) prompts from earlier sessions for confidentiality violations; propose sanitized rewrites.

### Module 13.2 — Prompt Injection Attacks & Defense Mechanisms (1.5 hrs)
**Key Topics**
- How prompt injection works: appending malicious instructions to security data
- Defense strategies: input sanitization, system prompt hardening, output validation
- Separating user input from instructions with clear delimiters

**Hands-On Lab:** Conduct adversarial testing — attempt 10+ prompt injection attacks against a security prompt built earlier in the course, document successful/unsuccessful attempts, and rebuild the prompt to resist them.

### Module 13.3 — Hallucination Mitigation & Verification Workflows (1.5 hrs)
**Key Topics**
- Hallucination types in security contexts: false positives, invented CVEs, fabricated malware
- Building verification workflows with confidence thresholds
- Audit trails for compliance and forensic review

**Hands-On Lab:** Build a verification workflow for a security analysis task from an earlier session; define escalation rules and confidence thresholds.

### Module 13.4 — AI Governance Policy Drafting (1.0 hr)
**Key Topics**
- Drafting an internal AI-usage policy for a security team
- Light alignment to NIST AI RMF for model-risk framing

**Hands-On Lab:** Draft a one-page internal AI governance policy covering approved use cases, prohibited data types, and escalation paths.

---

## SESSION 14: Claude API, CI/CD & Ticketing Integration (Automation — 4.0 hrs)
*Recommended for all roles*

### Module 14.1 — Claude API Fundamentals for Security Automation (1.0 hr)
**Key Topics**
- Messages API: requests, responses, roles, message history
- System prompts, model selection, streaming, and cost tracking

**Hands-On Lab:** Write a Python/Node script that sends security-focused prompts to the API and parses responses, handling errors and rate limits.

### Module 14.2 — Building Security Automation Pipelines (1.5 hrs)
**Key Topics**
- Log analysis pipeline: ingest → Claude analysis → structured findings → alerting
- CI/CD-integrated code scanning: GitLab pipeline → security check → Claude review → ticket creation
- Production guardrails: rate limiting, cost controls, monitoring

**Hands-On Lab:** Design and partially implement a security automation pipeline for the participant's own environment (log analysis or CI/CD-integrated scanning); document architecture and guardrails.

### Module 14.3 — Tool Use, MCP & Ticketing Integration (1.5 hrs)
**Key Topics**
- Tool use/function calling: letting Claude call security tools directly
- Model Context Protocol (MCP): connecting Claude to CVE databases, asset inventories, ticketing systems
- Designing secure tool schemas with validation and error handling

**Hands-On Lab:** Give Claude a tool (API endpoint or function) for CVE lookups or vulnerability data; build a prompt that uses the tool to analyze a security report and draft a ticket for a sandbox ticketing system (Jira/ServiceNow developer instance, or a mocked equivalent).

---

## Time Allocation Summary

| Track | Sessions | Hours |
|---|---|---|
| Foundation | 1–2 | 9.0 |
| SOC / SecOps | 3–4 | 10.0 |
| AppSec | 5–6 | 7.0 |
| Cloud Security | 7–8 | 10.0 |
| GRC / Compliance | 9–10 | 7.0 |
| Threat Intelligence | 11–12 | 8.0 |
| Secure AI Usage | 13 | 5.0 |
| Automation | 14 | 4.0 |
| **Total** | **14 sessions** | **60.0** |

## Materials & Assessment

**Materials provided:** Participant workbook per session; role-specific prompt template libraries; synthetic lab datasets (SIEM exports, vulnerable code repos, K8s manifests, threat intel documents); API integration script examples (Python/Node).

**Assessment:** Per-module lab checkpoints; track capstones at the end of each specialist track (Modules 4.4, 6.3/8.4, 10.3, 12.3); final project — design and present a Claude-powered security workflow for the participant's own role.

**Prerequisites:** Foundation (Sessions 1–2) — none, open to all security professionals. Specialist tracks — familiarity with the relevant domain tooling (SIEM, SAST, cloud console, compliance frameworks, as applicable). Session 14 — basic scripting familiarity (Python or Node) recommended.
