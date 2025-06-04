import subprocess

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
