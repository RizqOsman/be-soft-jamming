import subprocess
import json 
import re
import time
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "interface_roles.json"

def load_interface_roles():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def set_monitor_mode(interface: str):
    try:
        result = subprocess.run(
            ["airmon-ng", "start", interface],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return {
            "success": True,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_monitor_interfaces(prefix="wlx"):
    result = subprocess.run(["iwconfig"], capture_output=True, text=True)
    interfaces = []
    current = None

    for line in result.stdout.splitlines():
        if not line.startswith(" ") and line.strip():
            current = line.split()[0]
        if current and "Mode:Monitor" in line and current.startswith(prefix):
            interfaces.append(current)
    return interfaces

def get_rtl_interfaces_by_mode():
    result = subprocess.run(["iwconfig"], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    interfaces = []
    current_iface = None
    mode = None

    for line in lines:
        if not line.startswith(' ') and line.strip():  # line baru = nama interface
            match = re.match(r'^(wlx[\w\d]+)', line)
            if match:
                current_iface = match.group(1)
        if current_iface and "Mode:" in line:
            mode_match = re.search(r'Mode:(\w+)', line)
            if mode_match:
                mode = mode_match.group(1)
                interfaces.append({
                    "interface": current_iface,
                    "mode": mode
                })
                current_iface = None  # reset
    return interfaces

def is_monitor_mode(iface: str) -> bool:
    result = subprocess.run(["iwconfig", iface], capture_output=True, text=True)
    return "Mode:Monitor" in result.stdout

def auto_set_monitor_for_all_rtl():
    results = []
    rtl_ifaces = get_rtl_interfaces_by_mode()

    for item in rtl_ifaces:
        iface = item["interface"]
        mode = item["mode"]
        if mode != "Monitor":
            set_result = set_monitor_mode(iface)
            time.sleep(1)  # beri waktu udev/netplan settle
            results.append({
                "interface": iface,
                "prev_mode": mode,
                "converted": set_result["success"],
                "output": set_result["output"],
                "error": set_result["error"]
            })
        else:
            results.append({
                "interface": iface,
                "prev_mode": "Monitor",
                "converted": False,
                "output": "Already in monitor mode",
                "error": ""
            })

    return results
