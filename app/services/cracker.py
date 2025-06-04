import subprocess
import os

def crack_handshake(cap_path: str, wordlist_path: str):
    result_file = "crack_output.txt"
    with open(result_file, "w") as outfile:
        subprocess.run([
            "aircrack-ng", "-w", wordlist_path, "-b", "ANY_BSSID", cap_path
        ], stdout=outfile)
    return result_file if os.path.exists(result_file) else None
