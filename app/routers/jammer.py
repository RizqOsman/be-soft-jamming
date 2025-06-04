from fastapi import APIRouter, Query
from app.services.jammer import run_jammer_sweep
from app.services.logger import log_event

router = APIRouter()

@router.post("/sweep")
def start_jammer(interface: str = Query(...)):
    run_jammer_sweep(interface)
    log_event("jammer_sweep", interface, "channel 1-11")
    return {"status": "sweep_started"}
