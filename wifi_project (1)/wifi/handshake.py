import subprocess
import time

def capture_handshake(interface, target):
    ssid, bssid, channel, _ = target
    print(f"[+] Starting handshake capture on {ssid} (Channel {channel})")
    
    try:
        subprocess.run(["iwconfig", interface, "channel", channel], check=True)
        airodump = subprocess.Popen(["airodump-ng", "--bssid", bssid, "-c", channel, "-w", "handshake", interface])
        print("[+] Waiting for handshake (20s)...")
        time.sleep(20)
        airodump.terminate()
        print("[+] Handshake capture attempt complete.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to capture handshake: {e}")
