import subprocess
import time
import os

def capture_handshake(interface: str, bssid: str, channel: str, timeout: int = 60):
    output_file = "captured-handshake"
    cap_file = f"{output_file}-01.cap"

    subprocess.run(["iwconfig", interface, "channel", channel])
    proc = subprocess.Popen([
        "airodump-ng", "-c", channel, "--bssid", bssid, "-w", output_file, interface
    ])
    time.sleep(timeout)
    proc.terminate()
    subprocess.run(["pkill", "airodump-ng"])

    if os.path.exists(cap_file):
        return cap_file
    return None

