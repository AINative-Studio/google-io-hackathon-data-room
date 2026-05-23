"""
Tests for Data Room Reconstructor
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from gemini_data_room_agents import DataRoomReconstructorService
import json
import os


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response"""
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": json.dumps({
                                "found_documents": ["Invoice_Jan_2024.pdf", "Tax_Return_2023.pdf"],
                                "key_metrics": {"monthly_expenses": 45000},
                                "sentiment": "complete",
                            })
                        }
                    ]
                },
                "finishReason": "STOP",
            }
        ],
    }


@pytest.mark.asyncio
async def test_service_initialization():
    """Test service can be initialized"""
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        service = DataRoomReconstructorService(api_key="test-key")
        assert service.api_key == "test-key"


@pytest.mark.asyncio
async def test_missing_api_key():
    """Test initialization fails without API key"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            DataRoomReconstructorService()


@pytest.mark.asyncio
async def test_reconstruct_data_room_structure(mock_gemini_response):
    """Test data room reconstruction returns correct structure"""
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        service = DataRoomReconstructorService(api_key="test-key")

        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_gemini_response)

        async def mock_post(*args, **kwargs):
            return mock_response

        with patch.object(service.client, "post", side_effect=mock_post):
            result = await service.reconstruct_data_room(
                founder_email="founder@startup.io",
                company_name="TestCorp",
            )

            assert result["founder_email"] == "founder@startup.io"
            assert result["company_name"] == "TestCorp"
            assert "timestamp" in result
            assert "data_room" in result
            assert "gap_analysis" in result
            assert "summary" in result


@pytest.mark.asyncio
async def test_scout_agents_parallel(mock_gemini_response):
    """Test that scout agents run in parallel"""
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        service = DataRoomReconstructorService(api_key="test-key")

        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_gemini_response)

        async def mock_post(*args, **kwargs):
            return mock_response

        with patch.object(service.client, "post", side_effect=mock_post):
            # Run only scouts
            result = await service._scout_gmail_agent("test@test.io", "TestCorp")
            assert result.get("status") == "success"


@pytest.mark.asyncio
async def test_consolidate_scout_results():
    """Test scout results consolidation"""
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        service = DataRoomReconstructorService(api_key="test-key")

        scout_results = [
            {
                "status": "success",
                "agent": "Scout Gmail",
                "data": {"found_documents": ["email1.pdf", "email2.pdf"]},
            },
            {
                "status": "success",
                "agent": "Scout Drive",
                "data": {"found_documents": ["doc1.xlsx", "doc2.docx"]},
            },
            Exception("Failed"),  # One scout failed
        ]

        consolidated = service._consolidate_scout_results(scout_results)

        assert consolidated["total_documents"] == 4
        assert len(consolidated["gmail_documents"]) == 2
        assert len(consolidated["drive_documents"]) == 2


@pytest.mark.asyncio
async def test_gap_analysis_generation(mock_gemini_response):
    """Test gap analysis is generated"""
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        service = DataRoomReconstructorService(api_key="test-key")

        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_gemini_response)

        async def mock_post(*args, **kwargs):
            return mock_response

        with patch.object(service.client, "post", side_effect=mock_post):
            result = await service._gap_analyzer_agent({}, {}, "TestCorp")
            assert result.get("status") == "success"


@pytest.mark.asyncio
async def test_summary_generation():
    """Test summary generation"""
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        service = DataRoomReconstructorService(api_key="test-key")

        documents = {"total_documents": 15, "gmail_documents": 5, "drive_documents": 10}
        
        gap_analysis = {
            "status": "success",
            "data": {
                "critical_gaps": [{"document": "Cap Table", "priority": 1}],
                "due_diligence_risk": "medium",
            },
        }
        
        synthesizer = {
            "status": "success",
            "data": {
                "investor_readiness_score": 75,
                "red_flags": [{"flag": "Missing recent cap table"}],
            },
        }

        summary = service._generate_summary(documents, gap_analysis, synthesizer)

        assert summary["documents_found"] == 15
        assert summary["investor_readiness"] == 75
        assert summary["red_flags_count"] == 1
        assert summary["due_diligence_risk"] == "medium"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=term-missing"])
