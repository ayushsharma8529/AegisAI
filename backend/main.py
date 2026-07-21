from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from core.init_db import initialize_database
from core.scan_repository import get_all_scans
from fastapi import HTTPException
from core.scan_repository import get_scan_by_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    initialize_database()

app.include_router(router)

@app.get("/history")
def scan_history():
    return get_all_scans()
@app.get("/history/{scan_id}")
def scan_details(scan_id: int):

    result = get_scan_by_id(scan_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    return result