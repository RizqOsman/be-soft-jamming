from fastapi import APIRouter
from app.models.schema import AuthFloodRequest, DeauthRequest, HCXJammingRequest, MultiJamRequest
from app.services import attacker
from app.services.attacker import run_multi_interface_jamming


router = APIRouter()

@router.post("/auth_flood")
def auth_flood(data: AuthFloodRequest):
    attacker.run_auth_flood(["wlan1", "wlan2", "wlan3"], data.bssid, data.ssid, data.speed)
    return {"status": "running", "method": "auth_flood"}

@router.post("/deauth")
def deauth(data: DeauthRequest):
    for target in data.targets:
        attacker.run_deauth("wlan1", target.BSSID)
    return {"status": "running", "method": "deauth"}

@router.post("/hcx_jamming")
def hcx_jam(data: HCXJammingRequest):
    attacker.run_hcx_jamming("wlan0", data.channel, data.ssid)
    return {"status": "running", "method": "hcx_jamming"}

@router.post("/jam/multi")
def multi_jam(data: MultiJamRequest):
    try:
        used_ifaces = run_multi_interface_jamming(
            bssid=data.bssid,
            channel=data.channel,
            ssid=data.ssid,
            mode=data.mode,
            speed=data.speed,
            iface_count=data.iface_count
        )
        return {
            "status": "running",
            "method": data.mode,
            "interfaces_used": used_ifaces
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}