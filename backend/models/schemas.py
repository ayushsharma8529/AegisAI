from pydantic import BaseModel


class ScanRequest(BaseModel):
    target: str
    start_port: int = 1
    end_port: int = 1024


class ScanResponse(BaseModel):
    target: str
    status: str
    message: str
    findings: list
    analysis: str