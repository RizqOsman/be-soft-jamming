from fastapi import FastAPI
from app.routers import (
    scan,
    attack,
    jammer,
    logger,
    interface,
    bluetooth
)
from app.services.interface import auto_set_monitor_for_all_rtl

app = FastAPI(
    title="Soft Jamming WiFi Backend",
    description="API untuk melakukan scanning, jamming, dan serangan jaringan WiFi menggunakan interface RTL8814AU",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    print("🔧 Inisialisasi interface RTL8814AU ke mode Monitor...")
    result = auto_set_monitor_for_all_rtl()
    for iface in result:
        status = "✅" if iface["converted"] else "⚠️"
        print(f"{status} {iface['interface']} ({iface['prev_mode']}): {iface['output']}")

app.include_router(scan.router, prefix="/scan", tags=["Scan"])
app.include_router(attack.router, prefix="/attack", tags=["Attack"])
app.include_router(jammer.router, prefix="/jammer", tags=["Jammer"])
app.include_router(logger.router, prefix="/logs", tags=["Logs"])
app.include_router(interface.router, prefix="/interface", tags=["Interface"])
app.include_router(bluetooth.router, prefix="/bluetooth", tags=["Bluetooth"])
