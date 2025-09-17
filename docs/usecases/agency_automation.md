# Agency Automation

## Goal
- **Autopilot client delivery** so retainer agencies can execute SEO, paid media, and reporting packages without constant human orchestration.
- **Protect margin while scaling** by giving operators a control tower for briefs, approvals, and quality gates.

## Flow
1. **Intake:** Collect client briefs from Slack, HubSpot, or forms and normalize them into a Naestro plan template.
2. **Plan:** Planner agent decomposes deliverables (audits, keyword research, ad refreshes) with budgets, owners, and deadlines.
3. **Execute:** Specialist agents run connectors (Firecrawl, Sheets, Ads APIs) and attach results while policy agents guardrails outputs.
4. **Review:** Humans get a single Studio queue to approve, request fixes, or escalate.
5. **Handoff:** Package deliverables, notify clients, update CRM/project tools, and archive telemetry for audits.

## Components
- **Studio Agency Board** for intake, approvals, and SLA tracking.
- **Plan Template Library** seeded with SEO, paid media, and analytics deliverables.
- **Connector Mesh** (HubSpot, Notion, Google Ads, Sheets, Slack, Drive) orchestrated through Registry + Automations API.
- **QA & Policy Agents** running regression suites, content guidelines, and compliance checks before handoff.

## n8n Starter
- **Trigger:** HubSpot deal stage = "Kickoff" or Typeform brief submission.
- **Nodes:** Fetch brief → HTTP call to `/api/runs` with agency template → Slack DM to account lead → Wait for Naestro completion webhook → Upload outputs to Google Drive/Notion → close with HubSpot timeline note.
- **Operators:** Toggle between dry-run / live, with optional manual pause node for high-risk accounts.

## Rollout & Safety
- Start with a shadow pipeline mirroring existing manual delivery for two anchor clients.
- Require policy-guarded approval steps; enforce content QA + compliance prompts before outbound.
- Canary release automation per deliverable type (e.g., audits first, then campaign refreshes) with rollback to manual if defect rate > threshold.
- Capture full audit log (inputs, model calls, approvals) for every job and route escalations to incident channel.

## KPIs
- **Turnaround time** from brief to delivery (target: <24h for standard packages).
- **Automation coverage** (% of steps completed without manual work) and manual intervention rate.
- **Defect & rework rate** measured by QA flags or client reopen requests.
- **Retention & margin lift** (renewals, upsells, gross margin per retainer).
- **Operator workload** (runs per FTE, time-on-approval) to confirm scale benefits.
