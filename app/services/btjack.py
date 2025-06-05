import subprocess
import re

def scan_ble_btlejack(max_lines: int = 20):
    cmd = ["btlejack", "-s", "-d", "0"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    found = set()
    results = []

    try:
        for _ in range(max_lines):
            line = process.stdout.readline()
            match = re.search(
                r'Advertising address: ([\da-f:]+).*channel (\d+), RSSI (-?\d+)', line, re.IGNORECASE)
            if match:
                mac = match.group(1).lower()
                channel = match.group(2)
                rssi = int(match.group(3))
                if mac not in found:
                    found.add(mac)
                    results.append({
                        "address": mac,
                        "channel": channel,
                        "rssi": rssi
                    })
    finally:
        process.terminate()

    return results
