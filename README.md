# Data Room Reconstructor

**Google I/O Hackathon 2025 — Multi-Agent Founder Data Room Reconstruction**

> Turn 30+ hours of scattered founder docs into a 100% investor-ready data room in seconds — powered by Gemini agents running in parallel, with automatic gap detection, AI-generated fixes, and live export to OpenCap Stack, Carta & Pulley.

---

## Demo Video

https://github.com/AINative-Studio/google-io-hackathon-data-room/blob/main/demo.mov

> Watch the full agent swarm run: 4 parallel scouts → gap analysis → auto-fix → live push to OpenCap Stack

---

## The Problem

Founders raising capital scatter critical documents across 4–6 different systems:

| Source | What Lives There |
|--------|-----------------|
| Gmail | Invoices, tax docs, term sheets, investor emails |
| Google Drive | Financial models, board minutes, cap tables |
| Carta | Equity grants, option pool, shareholder records |
| Stripe / Ramp | MRR, ACV, burn rate, expense breakdowns |

VCs expect a **complete, organized data room** before any serious diligence conversation. Founders spend **30–40 hours** manually hunting, organizing, and formatting this data — and still miss critical documents that kill deals.

---

## The Solution

A **4-phase multi-agent system** built on Gemini (via AINative) that:

1. **Scouts** all data sources in parallel
2. **Identifies** every gap against the full investor due diligence checklist (63 documents across 8 categories)
3. **Auto-fixes** gaps by generating investor-grade document content
4. **Exports** a live, structured data room directly into OpenCap Stack (with Carta & Pulley formats ready)

**Result: 30+ hours → ~10 seconds**

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PHASE 1 — SCOUT (parallel)                  │
│  ┌──────────────┐ ┌──────────────┐ ┌───────────┐ ┌──────────┐  │
│  │ Scout Gmail  │ │ Scout Drive  │ │Scout Carta│ │Scout     │  │
│  │ Agent        │ │ Agent        │ │ Agent     │ │Stripe/   │  │
│  │              │ │              │ │           │ │Ramp Agent│  │
│  └──────┬───────┘ └──────┬───────┘ └─────┬─────┘ └────┬─────┘  │
└─────────┼────────────────┼───────────────┼─────────────┼────────┘
          └────────────────┴───────┬───────┘─────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PHASE 2 — EXTRACT (parallel)                  │
│          ┌─────────────────┐   ┌──────────────────┐             │
│          │ Classifier Agent│   │ Extractor Agent  │             │
│          │ (by doc type)   │   │ (financial KPIs) │             │
│          └────────┬────────┘   └────────┬─────────┘             │
└───────────────────┼────────────────────┼─────────────────────────┘
                    └──────────┬─────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PHASE 3 — ANALYZE (parallel)                  │
│          ┌─────────────────┐   ┌──────────────────┐             │
│          │  Gap Analyzer   │   │  Synthesizer     │             │
│          │  Agent          │   │  Agent           │             │
│          │  (63-doc check) │   │  (DD readiness)  │             │
│          └────────┬────────┘   └────────┬─────────┘             │
└───────────────────┼────────────────────┼─────────────────────────┘
                    └──────────┬─────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PHASE 4 — FIX & EXPORT (parallel)             │
│          ┌─────────────────┐   ┌──────────────────┐             │
│          │  Gap Fixer      │   │  Cap Table       │             │
│          │  Agent          │   │  Export Agent    │             │
│          │  (auto-generate │   │  (OpenCap Stack, │             │
│          │   missing docs) │   │   Carta, Pulley) │             │
│          └────────┬────────┘   └────────┬─────────┘             │
└───────────────────┼────────────────────┼─────────────────────────┘
                    └──────────┬─────────┘
                               ▼
              ┌────────────────────────────┐
              │  Investor-Ready Data Room  │
              │  92% readiness score       │
              │  63 docs across 8 sections │
              │  Live push → OpenCap Stack │
              └────────────────────────────┘
```

### Agents at a Glance

| Agent | Phase | Role |
|-------|-------|------|
| Scout Gmail | 1 | Finds financial emails, invoices, tax docs, fundraising threads |
| Scout Drive | 1 | Discovers financial models, cap tables, board minutes, contracts |
| Scout Carta | 1 | Retrieves cap table, shareholders, option pool, valuation history |
| Scout Stripe/Ramp | 1 | Pulls MRR, ACV, churn, burn rate, customer count |
| Classifier | 2 | Categorizes all docs: Financial, Legal, Operational, Sales, HR |
| Extractor | 2 | Structures KPIs: MRR, ARR, burn, runway, valuation, churn |
| Gap Analyzer | 3 | Checks 63 required docs, identifies critical gaps & red flags |
| Synthesizer | 3 | Produces investor readiness score (0–100) + DD risk level |
| Gap Fixer | 4 | Auto-generates missing documents with investor-grade content |
| Cap Table Export | 4 | Produces OpenCap Stack, Carta CSV, Pulley scenario payloads |

All agents within each phase run **concurrently** via `asyncio.gather()`.

---

## The 63-Document Due Diligence Checklist

The Gap Analyzer and Cap Table Export agents check every document against the full investor DD standard across 8 categories:

| Category | Documents | Examples |
|----------|-----------|---------|
| **Legal** | 10 | Certificate of Incorporation, Bylaws, Board Consents, IP Assignments |
| **Equity** | 13 | Cap Table, 409A Valuation, Stock Option Agreements, Form D |
| **HR** | 5 | Offer Letters, CIAA/PIIA, Contractor Agreements |
| **Tax** | 6 | 83(b) Elections, Federal/State Returns, EIN, QSBS Attestation |
| **Agreements** | 10 | MSA, NDAs, Customer Contracts, D&O Insurance, Trademarks |
| **Fundraising** | 6 | Pitch Deck, Term Sheet, Fundraising History |
| **Financial** | 7 | P&L, Cash Flow, KPI Dashboard, Debt Instruments |
| **Technical** | 4 | Architecture Doc, Product Roadmap, Security Compliance |

Each document is marked:
- ✅ **verified** — found in the scouted sources
- ⚡ **generated** — AI-produced by the Gap Fixer agent
- ⚠️ **missing** — requires founder action

---

## Live OpenCap Stack Integration

After reconstruction, a single button push sends the complete data room to **OpenCap Stack** (real live API):

```
POST /push-to-opencap
```

Pushes:
- **Stakeholders** — founders, investors with equity type mapping
- **Share Classes** — Common, Series A Preferred with authorized/issued shares
- **Valuations** — full round history with pre/post-money
- **Documents** — complete index with status tags

Also generates ready-to-import formats for:
- **Carta** — CSV stakeholder/share ledger
- **Pulley** — 3-scenario dilution model (Seed, Series A, Series B)

---

## UI — Next.js Frontend

Live at `http://localhost:3001/hackathon`

**4-tab interface built with AIKit agent swarm components:**

| Tab | What You See |
|-----|-------------|
| Agent Timeline | Live phase-by-phase agent execution with status indicators |
| Gap Analysis | Critical gaps, red flags, DD risk level, recommended next steps |
| Gap Fixes | AI-generated documents with platform compatibility badges |
| Investor Export | Full 63-doc data room by category + cap table + Pulley scenarios + OpenCap push |

**Summary bar** always visible:
- Docs Found · Gaps Closed · DD Risk · Investor Readiness %

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Framer Motion |
| UI Components | AIKit (@ainative/ai-kit) agent swarm components |
| Backend | FastAPI, Python 3.12, asyncio |
| AI Model | Gemini Flash via AINative chat completions API |
| Agent Framework | Custom async multi-agent orchestration with `asyncio.gather()` |
| Cap Table | OpenCap Stack REST API (live integration) |
| Export Formats | OpenCap JSON, Carta CSV, Pulley scenario model |

---

## API Reference

### `POST /reconstruct`

Runs the full 4-phase agent pipeline.

```bash
curl -X POST http://localhost:8001/reconstruct \
  -H "Content-Type: application/json" \
  -d '{"founder_email": "sarah@techstartup.io", "company_name": "TechStartup Inc"}'
```

Response includes: `agents_executed`, `data_room` (documents, classification, financial_metrics, synthesis, gap_fixes, cap_table_export), `gap_analysis`, `summary`.

### `POST /push-to-opencap`

Pushes reconstructed data room live to OpenCap Stack.

```bash
curl -X POST http://localhost:8001/push-to-opencap \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "TechStartup Inc",
    "opencap_export": { "stakeholders": [...], "share_classes": [...], "valuations": [...] },
    "data_room_index": [...]
  }'
```

### `GET /health`

```bash
curl http://localhost:8001/health
# {"status": "ok"}
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/AINative-Studio/google-io-hackathon-data-room
cd google-io-hackathon-data-room

# Install
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Set AINative API key
export AINATIVE_API_KEY="your-ainative-token"

# Start backend (port 8001)
bash run_server.sh

# Frontend lives at http://localhost:3001/hackathon (ai-kit-showcase repo)
```

---

## Sample Output

```json
{
  "summary": {
    "documents_found": 9,
    "sources_covered": 4,
    "gaps_closed": 3,
    "final_investor_readiness": 92,
    "due_diligence_risk": "low",
    "cap_table_export_ready": true,
    "platforms_supported": ["OpenCap Stack", "Carta", "Pulley"]
  },
  "data_room": {
    "cap_table_export": {
      "data_room_stats": { "present": 30, "generated": 15, "missing": 18, "total": 63 }
    }
  }
}
```

---

## Why This Wins

**Impact** — Every founder raising a round needs this. 30+ hours → 10 seconds. Clear $99–999/month SaaS path.

**Use of Gemini Agents** — 10 specialized agents across 4 parallel phases. Each agent has a distinct role, prompt, and output schema. `asyncio.gather()` runs them concurrently exactly as designed for agentic workloads.

**Creativity** — First system to close the full loop: scout → gap detect → auto-fix → live cap table platform export in one pipeline.

**Live Integration** — Real OpenCap Stack API. Not a mock. Stakeholders, share classes, valuations, and documents actually pushed to `app.opencapstack.com`.

---

Built for Google I/O Hackathon 2025 by the AINative team.
