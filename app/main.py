from fastapi import FastAPI
from app.routers import (
    scan,
    attack,
    jammer,
    logger,
    interface,
    bluetooth
)

app = FastAPI(
    title="Soft Jamming WiFi Backend",
    description="API untuk melakukan scanning, jamming, dan serangan jaringan WiFi menggunakan interface RTL8814AU",
    version="1.0.0"
)


app.include_router(scan.router, prefix="/scan", tags=["Scan"])
app.include_router(attack.router, prefix="/attack", tags=["Attack"])
app.include_router(jammer.router, prefix="/jammer", tags=["Jammer"])
app.include_router(logger.router, prefix="/logs", tags=["Logs"])
app.include_router(interface.router, prefix="/interface", tags=["Interface"])
app.include_router(bluetooth.router, prefix="/bluetooth", tags=["Bluetooth"])

