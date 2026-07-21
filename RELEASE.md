# Hermes MSP — v1.0 Release Notes

**Date:** 2026-07-21
**Status:** Production-ready. First client pending.

---

## Where We Started

July 17. Garry and I sat down and walked through the MSP product end to end. Not a code review. A smoke test. Pretend you're a client. Sign up. Get onboarded. Use the portal. What breaks?

Eighteen things broke.

Not cosmetic stuff. The credit system was theoretical — we couldn't meter or bill anyone. The portal was a single HTML file with no CI/CD, no staging, no way to deploy safely. No alerting. No ticket system. No fleet management. The unit economics were hand-wavy. The pricing had no renewal strategy. The delivery guarantee existed in conversation but not in the MSA.

We had a product that looked good in a demo and would have collapsed under a real client.

Four days later, every gap is closed. Here's what changed.

---

## What We Built

### The Foundation

We started with the plumbing. Without it, nothing else matters.

**Token routing and credit metering.** Every AI agent call routes through OpenRouter workspaces with per-client isolation. Usage is tracked per agent, per workflow, per client. The portal shows real costs. A T1 client's $200 monthly credit pool is enforced at the infrastructure level, not in a spreadsheet.

**Integration philosophy.** "We connect, we don't replace." Every integration level — API, Webhook, Export — is documented with clear boundaries. Clients know exactly what plugs into what.

**Core agent suite.** Six agents — Sales, Operations, Customer Success, Marketing, Finance, Support — each with structured context files, workflow skills, and deployment automation. Deploying a new client takes 2 minutes.

### The Product

Plumbing alone doesn't sell. We needed the product to be defensible.

**Tiered staffing model.** T1 gets business-hours response. T2 and T3 get after-hours coverage. The "who's answering at 3am" question has an answer now.

**Delivery guarantee.** If MAF fails to deliver for two consecutive months, the client walks. Full exit, no penalty. It's in the MSA — §14. Revenue sits in deferred until the monthly scorecard is delivered. This is a legal obligation, not a marketing line.

**Overage policy.** No hard caps. If a client exceeds their credit pool, they pay cost plus 20%. The OpenRouter budget is set at 3× the credit allocation as an infrastructure safety net. The client never sees a limit.

**Tweak vs new workflow matrix.** When a client asks for a change, the system classifies it. Minor config changes are tweaks — included. New workflows are change orders — billed. The ambiguity that kills scope conversations is gone.

**Data validation layer.** Every lead runs through schema, completeness, range, and duplicate checks before it touches the database. Bad data stops at the door.

### The Economics

With the product solid, we ran the actual numbers. Not projections. Math.

**Unit economics model.** LTV, CAC, break-even, funnel conversion — all modeled with formulas. T1 breaks even at month 4. T2 at month 3. T3 at month 2. Seventeen validation questions are built into the model. Change one number and the whole thing recalculates.

**T1 margin strategy.** T1 at $2,000 a month runs at 49.3% margin. That's below the 50% floor, but it's a loss leader for T2 and T3 upgrades. The math is documented. No hand-waving.

**Renewal pricing schedule.** Year 1 locks the rate. Year 2 increases 15%. Year 3 increases another 10%. Annual prepay gets a 10% discount. The schedule is published. It doesn't get negotiated per client.

**Pilot economics.** 60-day pilot at $1,000 a month. Conversion target: 80%. The pilot is the sales pitch. Show the before and after, make the gap obvious, and they can't say no.

### The Infrastructure

The last piece. The systems that keep everything running when nobody's watching.

**CI/CD safety rails.** Both repos have staging branches, GitHub Actions syntax checks, and Vercel preview deployments. Push to staging, auto-deploy preview, open a PR, syntax check runs, merge to main. The "it worked on my machine" era is over.

**Ticket resolver.** A cron job polls for unassigned tickets every 5 minutes. It classifies by category and priority, searches the knowledge base for similar resolved tickets, assigns a human, and sets an SLA deadline. Phase 1 is triage only. Phase 2 — auto-resolve — and Phase 3 — auto-implement — are waiting until we have real KB data from live clients. Building those against demo data would produce rules that don't match real tickets.

**Fleet update manager.** When the core agent suite gets updated, the fleet manager diffs the changes, runs a health check on staging, promotes to live, and rolls back if anything breaks. Low-risk updates auto-apply. High-risk updates wait for approval.

**Alerting pipeline.** Health checks run every 15 minutes across all clients. P0 — agent down — triggers SMS, email, Discord, and an auto-ticket. P1 — error rate above 10% — triggers email, Discord, and an auto-ticket. P2 — credit pool below 20% — triggers portal and email. P3 — warnings — are portal-only. The alert router Edge Function handles the routing. The portal shows a real-time alerts page with severity filters and acknowledge buttons.

---

## By the Numbers

| Metric | Count |
|--------|-------|
| Gaps closed | 16 of 18 (2 deferred — need real client data) |
| New Python | 1,653 lines across 3 scripts |
| New TypeScript | 3 Edge Functions |
| New SQL | 2 migrations |
| Portal growth | 3,435 to 3,554 lines |
| QA rounds | 3 swarms, 9 agents, 15+ bugs found and fixed |
| Cron jobs | 3 new |
| Docs written | 7 |

---

## What This Means for Clients

Before: a client signed up and got a demo portal with fake data, agents that might work, no way to track anything, and no guarantee anything would keep working.

Now: a client signs up and gets a dedicated OpenRouter workspace with per-client isolation, six AI agents deployed in 2 minutes, a real-time portal showing fleet health and ticket status and usage costs and alert history, automated ticket triage with SLA tracking, health checks every 15 minutes with P0 through P3 alert routing, a delivery guarantee in the MSA, clear pricing with a published renewal schedule, and documented integration boundaries.

The product went from "demo that would break under load" to "platform that can onboard a client in 30 minutes and keep them running."

---

## What's Deferred

Two items need real client data before they're worth building:

**Auto-resolve (Ticket Resolver Phase 2).** When a ticket matches a known KB pattern, auto-resolve it. Needs 20 to 30 resolved tickets with verified solutions before the patterns are reliable.

**Auto-implement (Ticket Resolver Phase 3).** For tweak tickets, propose and apply code or config changes automatically. Needs Phase 2 live plus real-world calibration of the tweak versus new-workflow boundary.

Two items were cancelled:

**Portal component split.** Splitting 3,554 lines into separate files adds a build step and breaks single-file deploy. Zero user-facing value.

**Next.js migration.** Static HTML on Vercel serves instantly with zero server cost. Next.js adds cold starts and build complexity for no benefit on an auth-gated dashboard.

---

## What's Next

The system is complete. The next milestone is a real T1 pilot.

When a client signs, follow the operator's manual. Six steps, 30 minutes:

1. Provision OpenRouter workspace
2. Deploy agent suite
3. Configure client profile
4. Register in fleet registry
5. Run SQL migrations
6. Verify with health check and ticket resolver

The platform handles the rest.

---

## Key Files

| File | What It Is |
|------|------------|
| `hermes-msp-gap-remediation-spec-2026-07-17.md` | The original 18-gap audit |
| `batch-0-milestone-2026-07-20.md` | Foundation: token routing, integration philosophy, core suite |
| `batch-1-milestone-2026-07-20.md` | Product: staffing, guarantee, overage, triage matrix, validation |
| `batch-2-milestone-2026-07-20.md` | Economics: margins, unit model, renewal pricing, pilot math |
| `batch-3-milestone-2026-07-20.md` | Infrastructure: CI/CD, tickets, fleet updates, alerting |
| `deferred-items-next-update-2026-07-21.md` | What's deferred, why, and what triggers each item |
| `operators-manual-2026-07-21.md` | What to do when a client signs |
| `unit-economics-2026-07-20.md` | Authoritative cost and margin model |
