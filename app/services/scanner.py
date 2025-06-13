import subprocess
import time
import os
import csv
import json
from datetime import datetime, timedelta
from app.services.utils import get_interfaces
from app.services.utils import parse_csv

SCAN_PID_FILE = "scan_pid.txt"
SCAN_FILENAME = "scan_live-01.csv"
SCAN_META_FILE = "scan_meta.json"

def check_interfaces():

    result = subprocess.run(["iwconfig"], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()
    interfaces = []
    current_iface = None
    mode = "Unknown"
    is_rtl8814au = False

    for line in lines:
        if not line.startswith(" ") and line.strip():
        
            if current_iface and is_rtl8814au:
                interfaces.append({"interface": current_iface, "mode": mode})
        
            current_iface = line.split()[0]
            mode = "Unknown"
            is_rtl8814au = False
        if "Mode:" in line:
            parts = line.split("Mode:")
            if len(parts) > 1:
                mode = parts[1].split()[0]
        if 'Nickname:"WIFI@RTL8814AU"' in line:
            is_rtl8814au = True


    if current_iface and is_rtl8814au:
        interfaces.append({"interface": current_iface, "mode": mode})

    return interfaces

def start_airodump(iface: str, duration: int = 30):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"scan_{timestamp}"
    filename = f"{output_file}-01.csv"

    try:
        proc = subprocess.Popen(
            ["airodump-ng", "-w", output_file, "--output-format", "csv", iface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(duration)

        proc.terminate()
        time.sleep(1)
        subprocess.run(["pkill", "-f", "airodump-ng"], stdout=subprocess.DEVNULL)

        for _ in range(10):
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                break
            time.sleep(1)

        if os.path.exists(filename):
            targets = parse_csv(filename)
            return {
                "filename": filename,
                "results": targets
            }
        else:
            return {"filename": filename, "results": []}

    except Exception as e:
        return {"error": str(e)}
    

def start_airodump_live(iface: str):
    try:
        proc = subprocess.Popen(
            ["airodump-ng", "-w", "scan_live", "--output-format", "csv", iface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        with open(SCAN_PID_FILE, "w") as f:
            f.write(str(proc.pid))

        return {"status": "scanning_started", "pid": proc.pid}
    
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
def start_airodump_with_duration(iface: str, duration: int):
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration)

    proc = subprocess.Popen(
        ["airodump-ng", "-w", "scan_live", "--output-format", "csv", iface],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    with open(SCAN_PID_FILE, "w") as f:
        f.write(str(proc.pid))

    with open(SCAN_META_FILE, "w") as f:
        json.dump({
            "iface": iface,
            "pid": proc.pid,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration": duration
        }, f)

    return {"status": "scanning_started", "pid": proc.pid}

def stop_airodump():
    try:
        if not os.path.exists(SCAN_PID_FILE):
            return {"status": "not_running"}

        with open(SCAN_PID_FILE, "r") as f:
            pid = int(f.read().strip())

        subprocess.run(["kill", "-9", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(SCAN_PID_FILE)

        # Tunggu file CSV valid
        for _ in range(10):
            if os.path.exists(SCAN_FILENAME) and os.path.getsize(SCAN_FILENAME) > 0:
                break
            time.sleep(1)

        if os.path.exists(SCAN_FILENAME):
            targets = parse_csv(SCAN_FILENAME)
            return {
                "status": "scan_stopped",
                "results": targets
            }
        else:
            return {"status": "no_data", "results": []}

    except Exception as e:
        return {"status": "error", "detail": str(e)}
    

def parse_csv(filepath):
    access_points = []

    with open(filepath, newline='', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        rows = list(reader)

    in_clients = False

    for row in rows:
        if not row:
            in_clients = True
            continue
        if in_clients:
            continue
        if len(row) >= 14:
            ap_data = {
                "bssid": row[0].strip(),
                "channel": row[3].strip(),
                "ssid": row[13].strip()
            }
            access_points.append(ap_data)

    return access_points

def get_scan_progress():
    if not os.path.exists(SCAN_META_FILE):
        return {"active": False}

    with open(SCAN_META_FILE, "r") as f:
        meta = json.load(f)

    now = datetime.now()
    start = datetime.fromisoformat(meta["start"])
    end = datetime.fromisoformat(meta["end"])

    if now > end:
        return {"active": False, "progress": 100}

    progress = int(((now - start).total_seconds() / (end - start).total_seconds()) * 100)

    return {
        "active": True,
        "iface": meta["iface"],
        "progress": min(progress, 100),
        "start": meta["start"],
        "end": meta["end"]
    }