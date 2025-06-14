import subprocess
import re

def run_jammer_sweep(interface: str):
    subprocess.Popen(["mdk4", interface, "d", "-c", "1-11"])

def get_active_jammer_interfaces():
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    jammer_procs = []

    for line in lines:
        if any(tool in line for tool in ["aireplay-ng", "mdk4", "hcxjamming"]):
            parts = line.split()
            pid = parts[1]
            cmdline = " ".join(parts[10:])  # ambil command full (after USER/PID/...)
            match = re.search(r"\s(wlx[\w\d]+|wlan\d+)", cmdline)
            iface = match.group(1) if match else "unknown"
            jammer_procs.append({
                "pid": pid,
                "tool": parts[10],
                "interface": iface,
                "cmd": cmdline
            })

    active_ifaces = list({proc["interface"] for proc in jammer_procs if proc["interface"] != "unknown"})

    return {
        "active_interfaces": active_ifaces,
        "count": len(active_ifaces),
        "details": jammer_procs
    }

def stop_jammer_on_interface(iface: str):
    procs = get_active_jammer_interfaces()

    for proc in procs:
        if proc["interface"] == iface:
            try:
                subprocess.run(["kill", "-9", proc["pid"]], check=True)
                return {
                    "interface": iface,
                    "killed": True,
                    "pid": proc["pid"],
                    "tool": proc["tool"]
                }
            except Exception as e:
                return {"interface": iface, "killed": False, "error": str(e)}
    return {"interface": iface, "killed": False, "error": "No matching jammer process found"}