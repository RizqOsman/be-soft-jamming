from pydantic import BaseModel
from typing import List, Literal

class Target(BaseModel):
    bssid: str
    channel: str
    ssid: str

class ScanResult(BaseModel):
    filename: str
    results: List[Target]

class AuthFloodRequest(BaseModel):
    bssid: str
    ssid: str
    speed: int

class DeauthRequest(BaseModel):
    targets: List[Target]

class RogueAPRequest(BaseModel):
    bssid: str
    channel: str
    ssid: str

class HCXJammingRequest(BaseModel):
    channel: str
    ssid: str

class MultiJamRequest(BaseModel):
    bssid: str
    channel: str
    ssid: str
    mode: Literal["auth", "deauth", "beacon", "hcx"]
    speed: int = 1000
    iface_count: int = 2
