from fastapi import APIRouter, Query
from app.services.interface import set_monitor_mode
from app.services.logger import log_event

router = APIRouter()

@router.post("/monitor")
def enable_monitor_mode(interface: str = Query(..., description="Interface WiFi seperti wlan0")):
    result = set_monitor_mode(interface)
    if result["success"]:
        log_event("enable_monitor", interface, "airmon-ng")
        return {"status": "ok", "message": result["output"]}
    else:
        return {"status": "error", "detail": result["error"]}
