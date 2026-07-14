from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from core.init_db import initialize_database
from core.scan_repository import get_all_scans

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
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