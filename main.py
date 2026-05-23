#!/usr/bin/env python3
"""
Data Room Reconstructor - FastAPI Server
Google I/O Hackathon 2025

Multi-agent system that reconstructs founder data rooms from scattered sources.
"""

import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from gemini_data_room_agents import DataRoomReconstructorService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Data Room Reconstructor",
    description="AI-powered founder data room reconstruction using Gemini agents via AINative",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENCAP_BASE = "https://api.opencapstack.com/api/v1"
OPENCAP_EMAIL = "benjamin@bvjconsulting.com"
OPENCAP_PASSWORD = "OpenCap2026!"


class DataRoomRequest(BaseModel):
    founder_email: str
    company_name: str = "StartupCorp"


class OpenCapPushRequest(BaseModel):
    company_name: str
    opencap_export: dict  # stakeholders, share_classes, valuations
    data_room_index: list


async def _opencap_token() -> str:
    """Login to OpenCap and return access token."""
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{OPENCAP_BASE}/auth/login",
            json={"email": OPENCAP_EMAIL, "password": OPENCAP_PASSWORD},
        )
        r.raise_for_status()
        return r.json()["accessToken"]


@app.get("/")
async def root():
    return FileResponse("dashboard.html", media_type="text/html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api")
async def api_root():
    return {
        "message": "📂 Data Room Reconstructor API",
        "endpoints": [
            "POST /reconstruct - Reconstruct founder data room",
            "POST /push-to-opencap - Push data room to OpenCap Stack",
            "GET /health - Health check",
        ],
    }


@app.post("/reconstruct")
async def reconstruct_data_room(request: DataRoomRequest):
    try:
        api_key = os.getenv("AINATIVE_API_KEY")
        if not api_key:
            raise ValueError("AINATIVE_API_KEY environment variable not set")

        service = DataRoomReconstructorService(api_key=api_key)
        logger.info(f"Reconstructing data room for {request.company_name} ({request.founder_email})...")
        result = await service.reconstruct_data_room(
            founder_email=request.founder_email,
            company_name=request.company_name,
        )
        logger.info(f"✅ Reconstruction complete: {result['summary']}")
        return result

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Reconstruction error: {e}")
        raise HTTPException(status_code=500, detail=f"Reconstruction failed: {str(e)}")


@app.post("/push-to-opencap")
async def push_to_opencap(request: OpenCapPushRequest):
    """
    Push reconstructed data room into OpenCap Stack:
    - Creates/updates stakeholders
    - Creates/updates share classes
    - Creates valuation
    - Creates document index entries
    """
    try:
        token = await _opencap_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        results = {"stakeholders": [], "share_classes": [], "valuations": [], "documents": [], "errors": []}

        async with httpx.AsyncClient(timeout=30) as client:

            # 1. Push stakeholders
            for s in request.opencap_export.get("stakeholders", []):
                try:
                    role = s.get("role", "Investor")
                    equity_type = "common" if "Founder" in role else "preferred"
                    r = await client.post(
                        f"{OPENCAP_BASE}/stakeholders",
                        headers=headers,
                        json={
                            "name": s.get("name"),
                            "email": s.get("email"),
                            "role": role,
                            "type": equity_type,
                        },
                    )
                    data = r.json()
                    results["stakeholders"].append({
                        "name": s.get("name"),
                        "status": "created" if r.status_code in (200, 201) else "error",
                        "id": data.get("_id") or data.get("id"),
                    })
                    logger.info(f"Stakeholder {s.get('name')}: {r.status_code}")
                except Exception as e:
                    results["errors"].append(f"Stakeholder {s.get('name')}: {e}")

            # 2. Push share classes
            for sc in request.opencap_export.get("share_classes", []):
                try:
                    r = await client.post(
                        f"{OPENCAP_BASE}/share-classes",
                        headers=headers,
                        json={
                            "name": sc.get("name"),
                            "type": "common" if "Common" in sc.get("name", "") else "preferred",
                            "parValue": 0.0001,
                            "authorizedShares": sc.get("authorized_shares", 10000000),
                            "boardApprovalDate": "2024-01-01",
                            "stockholderApprovalDate": "2024-01-01",
                        },
                    )
                    data = r.json()
                    results["share_classes"].append({
                        "name": sc.get("name"),
                        "status": "created" if r.status_code in (200, 201) else "error",
                        "id": data.get("_id") or data.get("id"),
                    })
                    logger.info(f"Share class {sc.get('name')}: {r.status_code}")
                except Exception as e:
                    results["errors"].append(f"Share class {sc.get('name')}: {e}")

            # 3. Push valuation
            for v in request.opencap_export.get("valuations", []):
                try:
                    r = await client.post(
                        f"{OPENCAP_BASE}/valuations",
                        headers=headers,
                        json={
                            "valuationDate": v.get("date", "2024-06-01"),
                            "preMoney": v.get("pre_money", 20000000),
                            "postMoney": v.get("post_money", 25000000),
                            "roundName": v.get("round_name", "Series A"),
                            "notes": f"Imported by Data Room Reconstructor — {request.company_name}",
                        },
                    )
                    data = r.json()
                    results["valuations"].append({
                        "round": v.get("round_name"),
                        "status": "created" if r.status_code in (200, 201) else "error",
                    })
                    logger.info(f"Valuation {v.get('round_name')}: {r.status_code}")
                except Exception as e:
                    results["errors"].append(f"Valuation: {e}")

            # 4. Push document index entries
            for doc in request.data_room_index[:10]:  # first 10 to avoid rate limits
                if doc.get("status") == "missing":
                    continue
                try:
                    r = await client.post(
                        f"{OPENCAP_BASE}/documents",
                        headers=headers,
                        json={
                            "name": doc.get("name"),
                            "type": doc.get("category", "Legal"),
                            "status": doc.get("status", "present"),
                            "description": f"Imported by AI Data Room Reconstructor. Status: {doc.get('status')}",
                            "uploadedAt": "2026-05-23",
                        },
                    )
                    results["documents"].append({
                        "name": doc.get("name"),
                        "status": "created" if r.status_code in (200, 201) else "skipped",
                    })
                    logger.info(f"Document {doc.get('name')}: {r.status_code}")
                except Exception as e:
                    results["errors"].append(f"Document {doc.get('name')}: {e}")

        results["summary"] = {
            "stakeholders_pushed": len([s for s in results["stakeholders"] if s["status"] == "created"]),
            "share_classes_pushed": len([s for s in results["share_classes"] if s["status"] == "created"]),
            "valuations_pushed": len([v for v in results["valuations"] if v["status"] == "created"]),
            "documents_pushed": len([d for d in results["documents"] if d["status"] == "created"]),
            "errors": len(results["errors"]),
            "opencap_url": "https://app.opencapstack.com",
        }

        logger.info(f"✅ OpenCap push complete: {results['summary']}")
        return {"success": True, "results": results}

    except Exception as e:
        logger.error(f"OpenCap push error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenCap push failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 70)
    print("🚀 Data Room Reconstructor Server Starting")
    print("=" * 70)
    print(f"AINative API Key: {'✓' if os.getenv('AINATIVE_API_KEY') else '✗'}")
    print(f"Server: http://localhost:8001")
    print(f"Docs: http://localhost:8001/docs")
    print("=" * 70 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8001)
