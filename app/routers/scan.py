from fastapi import APIRouter, Query
from app.services.scanner import check_interfaces, start_airodump
from app.models.schema import Target, ScanResult

router = APIRouter()

@router.get("/interfaces", response_model=list)
def get_monitor_interfaces():
    return check_interfaces()

@router.get("/ssid", response_model=list[Target])
def scan_ssids(iface: str, duration: int = Query(30, ge=10, le=180)):
    result = start_airodump(iface, duration)
    return result["results"]

