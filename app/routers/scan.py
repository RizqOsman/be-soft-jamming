from fastapi import APIRouter, Query
from app.services.scanner import (
    check_interfaces, 
    start_airodump, 
    start_airodump_live, 
    stop_airodump, 
    start_airodump_with_duration, 
    get_scan_progress
)

from app.models.schema import Target

router = APIRouter()

@router.get("/interfaces", response_model=list)
def get_monitor_interfaces():
    return check_interfaces()

@router.get("/ssid", response_model=list[Target])
def scan_ssids(iface: str, duration: int = Query(30, ge=10, le=180)):
    result = start_airodump(iface, duration)
    return result["results"]

@router.post("/start/scan", response_model=dict)
def start_scan_live(iface: str):
    return start_airodump_live(iface)

@router.post("/start/scan", response_model=dict)
def start_scan(iface: str, duration: int = Query(30, ge=10, le=180)):
    return start_airodump_with_duration(iface, duration)

@router.post("/stop/scan", response_model=list[Target])
def stop_scan_live():
    result = stop_airodump()
    return result["results"]

@router.get("/progress", response_model=dict)
def scan_progress():
    return get_scan_progress()
