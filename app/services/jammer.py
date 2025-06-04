import subprocess

def run_jammer_sweep(interface: str):
    subprocess.Popen(["mdk4", interface, "d", "-c", "1-11"])
