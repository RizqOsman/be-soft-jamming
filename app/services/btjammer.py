import subprocess

def run_bt_scan():
    subprocess.Popen(["btlejack", "-s"])

def run_bt_jam(channel: int = 37):
    subprocess.Popen(["btlejack", "-j", "-c", str(channel)])