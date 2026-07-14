from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from models.schemas import ScanRequest, ScanResponse
from services.scanner import run_scan
from services.report_generator import generate_html_report
from ai.analyzer import generate_analysis
from core.scan_repository import save_scan
from core.scan_repository import get_all_scans

LAST_SCAN = None

router = APIRouter()


@router.get("/status")
def status():
    return {
        "service": "AegisAI",
        "status": "online"
    }


@router.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):

    global LAST_SCAN

    result = run_scan(
        request.target,
        request.start_port,
        request.end_port
    )

    result["analysis"] = generate_analysis(
        result["findings"]
    )
    save_scan(result)

    LAST_SCAN = result

    return result


@router.get("/report", response_class=HTMLResponse)
def report():

    global LAST_SCAN

    if LAST_SCAN is None:
        return "<h2>No scan has been performed yet.</h2>"

    return generate_html_report(LAST_SCAN)
@router.get("/history")
def history():

    scans = get_all_scans()

    return [
        {
            "id": row[0],
            "target": row[1],
            "status": row[2],
            "created_at": row[3]
        }
        for row in scans
    ]