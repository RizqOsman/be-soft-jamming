from fastapi import APIRouter, Query
from app.services.handshake import capture_handshake
from app.services.logger import log_event

router = APIRouter()

@router.post("/start")
def start_handshake_capture(
    iface: str = Query(...),
    bssid: str = Query(...),
    channel: str = Query(...),
    timeout: int = Query(60)
):
    cap_file = capture_handshake(iface, bssid, channel, timeout)
    if cap_file:
        log_event("handshake_capture", iface, bssid)
        return {"status": "success", "file": cap_file}
    return {"status": "failed", "reason": "No handshake captured"}
