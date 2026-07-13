from fastapi import APIRouter
from ai.analyzer import generate_analysis
from models.schemas import ScanRequest, ScanResponse
from services.scanner import run_scan

router = APIRouter()


@router.get("/status")
def status():
    return {
        "service": "AegisAI",
        "status": "online"
    }


@router.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):

    result = run_scan(
        request.target,
        request.start_port,
        request.end_port
    )

    result["analysis"] = generate_analysis(
        result["findings"]
    )

    return result