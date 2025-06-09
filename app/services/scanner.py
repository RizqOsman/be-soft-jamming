import subprocess
import time
import os
import csv
from datetime import datetime
from app.services.utils import parse_csv

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
    # Gunakan timestamp agar filename unik
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"scan_{timestamp}"
    filename = f"{output_file}-01.csv"

    try:
        # Jalankan airodump-ng
        proc = subprocess.Popen(
            ["airodump-ng", "-w", output_file, "--output-format", "csv", iface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Tunggu proses scan
        time.sleep(duration)

        # Hentikan proses dengan aman
        proc.terminate()
        time.sleep(1)
        subprocess.run(["pkill", "-f", "airodump-ng"], stdout=subprocess.DEVNULL)

        # Tunggu file hasil dibuat
        for _ in range(10):
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                break
            time.sleep(1)

        # Parse hasil scan
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