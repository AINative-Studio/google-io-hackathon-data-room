#!/usr/bin/env python3
"""
Data Room Reconstructor - FastAPI Server
Google I/O Hackathon 2025

Multi-agent system that reconstructs founder data rooms from scattered sources.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_data_room_agents import DataRoomReconstructorService
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Data Room Reconstructor",
    description="AI-powered founder data room reconstruction using Gemini 2.5 Flash",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response schemas
class DataRoomRequest(BaseModel):
    """Data room reconstruction request"""
    founder_email: str
    company_name: str = "StartupCorp"


class DataRoomResponse(BaseModel):
    """Data room reconstruction response"""
    founder_email: str
    company_name: str
    timestamp: str
    agents_executed: list = []
    data_room: dict
    gap_analysis: dict
    summary: dict


# Routes
@app.get("/")
async def root():
    """Dashboard UI"""
    return FileResponse("dashboard.html", media_type="text/html")


@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "📂 Data Room Reconstructor API",
        "endpoints": [
            "POST /reconstruct - Reconstruct founder data room",
            "GET /health - Health check",
        ],
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}


@app.post("/reconstruct")
async def reconstruct_data_room(request: DataRoomRequest):
    """
    Reconstruct founder's data room from scattered sources
    
    Uses 5 specialized agents running in parallel:
    1. Scout agents (4) - Discover docs from Gmail, Drive, Carta, Stripe/Ramp
    2. Classifier agent - Categorizes documents
    3. Extractor agent - Pulls structured financial data
    4. Gap Analyzer agent - Identifies missing documents
    5. Synthesizer agent - Creates clean data room view + red-flag report
    
    Returns complete data room with investor-ready structure and gap analysis.
    """
    try:
        # Initialize service
        api_key = os.getenv("AINATIVE_API_KEY")
        if not api_key:
            raise ValueError("AINATIVE_API_KEY environment variable not set")

        service = DataRoomReconstructorService(api_key=api_key)

        # Run analysis
        logger.info(f"Reconstructing data room for {request.company_name} ({request.founder_email})...")
        result = await service.reconstruct_data_room(
            founder_email=request.founder_email,
            company_name=request.company_name,
        )

        logger.info(f"✅ Reconstruction complete: {result['summary']}")
        return DataRoomResponse(**result)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Reconstruction error: {e}")
        raise HTTPException(status_code=500, detail=f"Reconstruction failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    # Run server
    print("\n" + "=" * 70)
    print("🚀 Data Room Reconstructor Server Starting")
    print("=" * 70)
    print(f"AINative API Key configured: {'✓' if os.getenv('AINATIVE_API_KEY') else '✗'}")
    print(f"Server running at: http://localhost:8000")
    print(f"Docs at: http://localhost:8000/docs")
    print("=" * 70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
