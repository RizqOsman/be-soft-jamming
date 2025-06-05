from fastapi import APIRouter
from app.models.schema import BTJamRequest
from app.services.btjack import scan_ble_btlejack
import subprocess

router = APIRouter()

@router.post("/bt/jam")
def bt_soft_jam(data: BTJamRequest):
    if data.mode == "scan":
        subprocess.Popen(["btlejack", "-s"])  # scan
    elif data.mode == "jam":
        subprocess.Popen(["btlejack", "-j", "-c", str(data.channel)])
    else:
        return {"error": "Invalid mode"}

    return {"status": "running", "mode": data.mode}


@router.get("/btlejack/scan")
def bluetooth_btlejack_scan():
    results = scan_ble_btlejack()
    return {
        "status": "ok",
        "count": len(results),
        "devices": results
    }

