from fastapi import APIRouter, Query
from app.services.jammer import run_jammer_sweep
from app.services.logger import log_event
from app.services.jammer import get_active_jammer_interfaces, stop_jammer_on_interface

router = APIRouter()

@router.post("/sweep")
def start_jammer(interface: str = Query(...)):
    run_jammer_sweep(interface)
    log_event("jammer_sweep", interface, "channel 1-11")
    return {"status": "sweep_started"}

@router.get("/status")
def jammer_status():
    return get_active_jammer_interfaces()


@router.post("/stop")
def stop_jammer(iface: str = Query(..., description="Interface to stop jammer")):
    return stop_jammer_on_interface(iface)