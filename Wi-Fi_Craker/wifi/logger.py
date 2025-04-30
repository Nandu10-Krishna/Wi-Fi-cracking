def log_result(ssid, password):
    try:
        with open("results.txt", "a") as f:
            f.write(f"SSID: {ssid} | Password: {password}
")
    except IOError as e:
        print(f"[-] Failed to log result: {e}")
