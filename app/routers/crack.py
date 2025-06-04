from fastapi import APIRouter, Query
from app.services.cracker import crack_handshake
from app.services.logger import log_event

router = APIRouter()

@router.post("/start")
def start_crack(
    cap_file: str = Query(...),
    wordlist: str = Query("wordlists/rockyou.txt")
):
    result_file = crack_handshake(cap_file, wordlist)
    if result_file:
        log_event("crack_attempt", "-", cap_file)
        with open(result_file, "r") as f:
            content = f.read()
        return {"status": "done", "result": content}
    return {"status": "failed", "reason": "Crack file not generated"}
