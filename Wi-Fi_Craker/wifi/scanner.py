import subprocess
import time
import os

def scan_networks(interface="wlan0mon", scan_time=10):
    print(f"[+] Scanning for networks on {interface}...")
    dumpfile = "scan_results"
    cmd = ["airodump-ng", interface, "--write", dumpfile, "--output-format", "csv"]
    
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(scan_time)
        proc.terminate()
        time.sleep(2)
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to scan networks: {e}")
        return []

    csv_file = f"{dumpfile}-01.csv"
    if not os.path.exists(csv_file):
        print("[-] Scan results not found.")
        return []

    networks = []
    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
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
    print("
Available Networks:")
    for i, net in enumerate(networks):
        print(f"[{i}] SSID: {net[0]} | BSSID: {net[1]} | Channel: {net[2]} | Signal: {net[3]}")
    while True:
        try:
            choice = int(input("Select target network by number: "))
            if 0 <= choice < len(networks):
                return networks[choice]
            else:
                print("[!] Invalid selection. Try again.")
        except ValueError:
            print("[!] Please enter a valid number.")
