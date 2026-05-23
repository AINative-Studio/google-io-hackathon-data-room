"""
Gemini Multi-Agent Data Room Reconstructor
Google I/O Hackathon 2025

Reconstructs founder data rooms from scattered sources using 5 specialized agents:
1. Scout Agents (4) - Scout Gmail, Drive, Carta, Stripe/Ramp (mocked)
2. Classifier Agent - Categorizes documents by type
3. Extractor Agent - Pulls structured financial data
4. Gap Analyzer Agent - Identifies missing documents
5. Synthesizer Agent - Creates clean data room view + red-flag report
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
import logging
import httpx
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class DataRoomReconstructorService:
    """
    Orchestrates Gemini agents to reconstruct founder data rooms
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable required")
        self.base_url = "https://generativelanguage.googleapis.com/v1"
        self.client = httpx.AsyncClient(timeout=120.0)

    async def reconstruct_data_room(
        self, founder_email: str, company_name: str = "StartupCorp"
    ) -> Dict[str, Any]:
        """
        Orchestrate all agents to reconstruct founder's data room
        
        Agents (run in parallel):
        1. Scout Gmail Agent - Finds financial emails
        2. Scout Drive Agent - Discovers financial documents
        3. Scout Carta Agent - Retrieves cap table & funding info
        4. Scout Stripe/Ramp Agent - Gets payment processor data
        5. Classifier Agent - Categorizes all documents
        6. Extractor Agent - Pulls structured financial metrics
        7. Gap Analyzer Agent - Identifies missing critical docs
        8. Synthesizer Agent - Creates clean data room + report
        
        Args:
            founder_email: Founder's email address
            company_name: Company name for context
            
        Returns:
            Complete data room reconstruction with red-flag analysis
        """
        
        # Phase 1: Scout agents run in parallel (gather raw documents)
        scout_tasks = [
            self._scout_gmail_agent(founder_email, company_name),
            self._scout_drive_agent(founder_email, company_name),
            self._scout_carta_agent(founder_email, company_name),
            self._scout_stripe_ramp_agent(founder_email, company_name),
        ]
        
        logger.info("🔍 Phase 1: Scouting data sources in parallel...")
        scout_results = await asyncio.gather(*scout_tasks, return_exceptions=True)
        
        # Consolidate scout results
        gathered_documents = self._consolidate_scout_results(scout_results)
        
        # Phase 2: Classification & Extraction agents run in parallel
        logger.info("📂 Phase 2: Classifying & extracting data...")
        classification_task = self._classifier_agent(gathered_documents, company_name)
        extraction_task = self._extractor_agent(gathered_documents, company_name)
        
        classification_result, extraction_result = await asyncio.gather(
            classification_task, extraction_task, return_exceptions=True
        )
        
        # Phase 3: Gap Analysis & Synthesis run in parallel
        logger.info("🔎 Phase 3: Analyzing gaps & synthesizing data room...")
        gap_analysis_task = self._gap_analyzer_agent(
            gathered_documents, classification_result, company_name
        )
        synthesizer_task = self._synthesizer_agent(
            gathered_documents, classification_result, extraction_result, company_name
        )
        
        gap_analysis_result, synthesizer_result = await asyncio.gather(
            gap_analysis_task, synthesizer_task, return_exceptions=True
        )
        
        # Aggregate results
        return {
            "founder_email": founder_email,
            "company_name": company_name,
            "timestamp": datetime.utcnow().isoformat(),
            "data_room": {
                "documents": gathered_documents,
                "classification": classification_result if not isinstance(classification_result, Exception) else {},
                "financial_metrics": extraction_result if not isinstance(extraction_result, Exception) else {},
                "synthesis": synthesizer_result if not isinstance(synthesizer_result, Exception) else {},
            },
            "gap_analysis": gap_analysis_result if not isinstance(gap_analysis_result, Exception) else {},
            "summary": self._generate_summary(
                gathered_documents,
                gap_analysis_result,
                synthesizer_result
            ),
        }

    async def _scout_gmail_agent(self, founder_email: str, company_name: str) -> Dict[str, Any]:
        """Scout Gmail for financial emails"""
        prompt = f"""You are a data scout agent. Find financial emails for {company_name} founder ({founder_email}).
        
        Mock data: Assume the following emails exist:
        - Invoice from Brex (Business Expenses: $45,000/month)
        - Email from Stripe (Processing $250k/month in revenue)
        - Tax documents from accountant (Annual revenue: $2.8M)
        - Fundraising related emails (mentions $500k seed round)
        
        Return JSON with:
        - found_documents: list of document summaries
        - key_metrics: any financial figures mentioned
        - sentiment: "complete" or "missing_key_items"
        
        Format as JSON array of document objects."""
        
        return await self._call_gemini_agent(prompt, "Scout Gmail")

    async def _scout_drive_agent(self, founder_email: str, company_name: str) -> Dict[str, Any]:
        """Scout Google Drive for financial documents"""
        prompt = f"""You are a data scout agent. Find financial documents for {company_name} in Google Drive.
        
        Mock data: Assume the following documents exist:
        - Financial Model 2024 (spreadsheet with revenue projections)
        - Cap Table v3.2 (shows 5M shares outstanding, 1M options)
        - Board Meeting Minutes Q1 2024 (discusses Series A strategy)
        - Cash Flow Forecast (runway: 14 months at current burn)
        - Customer Contracts (3 enterprise customers)
        
        Return JSON with:
        - found_documents: list with filenames and summaries
        - key_insights: important findings
        - file_status: "complete" or "outdated" or "missing"
        
        Format as JSON array of document objects."""
        
        return await self._call_gemini_agent(prompt, "Scout Drive")

    async def _scout_carta_agent(self, founder_email: str, company_name: str) -> Dict[str, Any]:
        """Scout Carta for cap table & funding info"""
        prompt = f"""You are a data scout agent. Retrieve cap table and funding information for {company_name} from Carta.
        
        Mock data: Assume the following data exists in Carta:
        - Total Shares Outstanding: 5,000,000
        - Option Pool: 1,000,000 (20%)
        - Founder Equity: 50% (2.5M shares)
        - Series A Investors: Sequoia (30%), Kleiner Perkins (15%), Angels (5%)
        - Last Valuation: $25M (Series A - 6 months ago)
        - Outstanding Equity: 15% uncommitted from option pool
        
        Return JSON with:
        - shareholders: list with name, shares, percentage
        - capitalization_table: structured data
        - valuation_history: past valuations
        - dilution_analysis: founder ownership over time
        
        Format as structured JSON."""
        
        return await self._call_gemini_agent(prompt, "Scout Carta")

    async def _scout_stripe_ramp_agent(self, founder_email: str, company_name: str) -> Dict[str, Any]:
        """Scout Stripe & Ramp for payment processor data"""
        prompt = f"""You are a data scout agent. Retrieve payment & expense data for {company_name} from Stripe and Ramp.
        
        Mock data: Assume the following data exists:
        - Stripe:
          * Monthly Recurring Revenue (MRR): $250k
          * Annual Contract Value (ACV): $3.2M
          * Churn Rate: 2% MoM
          * Customer Count: 47 (3 enterprise, 44 SMB)
          * Payment Success Rate: 99.2%
        
        - Ramp:
          * Monthly Spend: $45k
          * Expense Categories: Software (40%), Contractor (35%), Infrastructure (25%)
          * Burn Rate: $42k/month
          * Vendor Count: 23
        
        Return JSON with:
        - stripe_metrics: MRR, ACV, churn, customer_count
        - ramp_metrics: monthly_spend, categories, burn_rate
        - cash_analysis: runway estimate
        
        Format as structured JSON."""
        
        return await self._call_gemini_agent(prompt, "Scout Stripe/Ramp")

    async def _classifier_agent(self, documents: Dict[str, Any], company_name: str) -> Dict[str, Any]:
        """Classify documents by type"""
        prompt = f"""You are a document classifier for {company_name}'s data room.
        
        Documents found:
        {json.dumps(documents, indent=2)[:2000]}  # First 2000 chars
        
        Classify each document into categories:
        - Financial (cap table, p&l, cash flow, etc)
        - Legal (articles of incorporation, contracts, etc)
        - Operational (board minutes, org chart, etc)
        - Sales (customer contracts, pipeline, etc)
        - HR (option pool, equity docs, etc)
        
        Return JSON with:
        - classification_by_type: {type: [documents]}
        - completeness_score: 0-100
        - categories_present: list of found categories
        - categories_missing: list of missing categories
        
        Format as structured JSON."""
        
        return await self._call_gemini_agent(prompt, "Classifier")

    async def _extractor_agent(self, documents: Dict[str, Any], company_name: str) -> Dict[str, Any]:
        """Extract structured financial metrics"""
        prompt = f"""You are a financial data extractor for {company_name}.
        
        From the documents, extract structured financial metrics:
        
        Revenue Metrics:
        - Monthly Recurring Revenue (MRR)
        - Annual Contract Value (ACV)
        - Total Revenue
        - Customer Count
        - Churn Rate
        
        Valuation Metrics:
        - Current Valuation
        - Fully Diluted Shares
        - Price per Share
        - Previous Valuations
        
        Financial Health:
        - Monthly Burn Rate
        - Runway (months)
        - Cash Balance
        - Profitability Status
        
        Return JSON with all found metrics. Use null for missing data."""
        
        return await self._call_gemini_agent(prompt, "Extractor")

    async def _gap_analyzer_agent(
        self, documents: Dict[str, Any], classification: Dict[str, Any], company_name: str
    ) -> Dict[str, Any]:
        """Identify missing critical documents"""
        prompt = f"""You are a gap analyzer for {company_name}'s data room.
        
        You have classified these documents:
        {json.dumps(classification, indent=2)[:1500]}
        
        Identify CRITICAL MISSING DOCUMENTS:
        
        Financial (Priority 1):
        - Cap table (current)
        - P&L statement (last 12 months)
        - Cash flow forecast (next 12 months)
        - Customer concentration analysis
        - Unit economics breakdown
        
        Legal (Priority 1):
        - Articles of Incorporation
        - Option pool documentation
        - Material contracts (>$50k annual)
        - IP assignment agreements
        
        Operational (Priority 2):
        - Board meeting minutes (last 6)
        - Org chart
        - Key hire agreements
        - Customer reference list
        
        Return JSON with:
        - critical_gaps: list of documents (name, priority, impact)
        - red_flags: list of concerning absences
        - due_diligence_risk: "high", "medium", "low"
        - recommended_next_steps: list
        
        Format as structured JSON."""
        
        return await self._call_gemini_agent(prompt, "Gap Analyzer")

    async def _synthesizer_agent(
        self,
        documents: Dict[str, Any],
        classification: Dict[str, Any],
        extraction: Dict[str, Any],
        company_name: str,
    ) -> Dict[str, Any]:
        """Create clean data room view + red-flag report"""
        prompt = f"""You are synthesizing {company_name}'s data room for investors.
        
        You have:
        - Documents: {len(documents)} found
        - Classification: {json.dumps(classification, indent=2)[:1000]}
        - Extraction: {json.dumps(extraction, indent=2)[:1000]}
        
        Create a professional data room view with:
        
        1. Executive Summary:
           - Company overview
           - Key metrics
           - Growth trajectory
        
        2. Organized Data Room Structure:
           - Financial Statements
           - Legal Documents
           - Operational Docs
           - Sales & Customer Info
           - Team & HR
        
        3. Red Flag Report:
           - Missing critical documents
           - Inconsistencies or concerns
           - Areas needing clarification
           - Investor diligence risks
           - Recommended follow-ups
        
        Return JSON with:
        - data_room_structure: organized hierarchy
        - executive_summary: 2-3 paragraph overview
        - key_metrics: most important numbers
        - red_flags: [{flag, severity, impact}]
        - investor_readiness_score: 0-100
        - next_steps_for_founder: list of priorities
        
        Format as professional JSON suitable for investor review."""
        
        return await self._call_gemini_agent(prompt, "Synthesizer")

    async def _call_gemini_agent(self, prompt: str, agent_name: str) -> Dict[str, Any]:
        """Call Gemini 3.5 Flash with the prompt"""
        try:
            url = f"{self.base_url}/models/gemini-3.5-flash:generateContent?key={self.api_key}"

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}],
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,  # Low temp for consistent analysis
                    "maxOutputTokens": 4096,  # Larger output for complex data
                },
            }

            response = await self.client.post(url, json=payload)
            response.raise_for_status()

            data = response.json()

            # Extract response content
            content = ""
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    content = " ".join([part.get("text", "") for part in parts])

            # Parse JSON from response
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    json_str = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    json_str = content[json_start:json_end].strip()
                else:
                    json_str = content

                result = json.loads(json_str)
                return {
                    "status": "success",
                    "agent": agent_name,
                    "data": result,
                }
            except json.JSONDecodeError:
                return {
                    "status": "success",
                    "agent": agent_name,
                    "data": {"raw_analysis": content},
                }

        except Exception as e:
            logger.error(f"Gemini agent {agent_name} error: {e}")
            return {
                "status": "error",
                "agent": agent_name,
                "error": str(e),
            }

    def _consolidate_scout_results(self, scout_results: List[Any]) -> Dict[str, Any]:
        """Consolidate results from all scout agents"""
        consolidated = {
            "gmail_documents": [],
            "drive_documents": [],
            "carta_data": {},
            "stripe_ramp_data": {},
            "total_documents": 0,
        }
        
        for i, result in enumerate(scout_results):
            if isinstance(result, Exception):
                logger.warning(f"Scout {i} failed: {result}")
                continue
            
            if result.get("status") != "success":
                continue
            
            agent = result.get("agent", "")
            data = result.get("data", {})
            
            if "Gmail" in agent:
                consolidated["gmail_documents"] = data.get("found_documents", [])
            elif "Drive" in agent:
                consolidated["drive_documents"] = data.get("found_documents", [])
            elif "Carta" in agent:
                consolidated["carta_data"] = data
            elif "Stripe" in agent:
                consolidated["stripe_ramp_data"] = data
        
        consolidated["total_documents"] = (
            len(consolidated["gmail_documents"]) +
            len(consolidated["drive_documents"])
        )
        
        return consolidated

    def _generate_summary(
        self, 
        documents: Dict[str, Any],
        gap_analysis: Any,
        synthesizer: Any
    ) -> Dict[str, Any]:
        """Generate summary statistics"""
        summary = {
            "documents_found": documents.get("total_documents", 0),
            "sources_covered": len([k for k in documents.keys() if documents[k]]),
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if isinstance(gap_analysis, dict) and gap_analysis.get("status") == "success":
            data = gap_analysis.get("data", {})
            summary["critical_gaps"] = len(data.get("critical_gaps", []))
            summary["due_diligence_risk"] = data.get("due_diligence_risk", "unknown")
        
        if isinstance(synthesizer, dict) and synthesizer.get("status") == "success":
            data = synthesizer.get("data", {})
            summary["investor_readiness"] = data.get("investor_readiness_score", 0)
            summary["red_flags_count"] = len(data.get("red_flags", []))
        
        return summary
