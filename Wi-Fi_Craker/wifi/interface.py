import subprocess

def setup_interface():
    interface = "wlan0"
    try:
        print(f"[+] Setting {interface} to monitor mode...")
        subprocess.run(["airmon-ng", "start", interface], check=True)
        return interface + "mon"
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to set {interface} to monitor mode: {e}")
        return None
