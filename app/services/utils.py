import csv

def parse_csv(filename):
    targets = []
    seen_ssids = set()

    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        print(filename, "PEAAAAAA")
        reader = csv.reader(f)
        print(reader)
        ssid_section = False
        for row in reader:
            # Strip spasi dari semua elemen row
            row = [cell.strip() for cell in row]
            
            print("ROW DEBUG:", row)

            if "BSSID" in row and "ESSID" in row:
                ssid_section = True
                continue

            if ssid_section:
                if len(row) < 14:
                    continue
                try:
                    bssid = row[0].strip()
                    channel = row[3].strip()
                    ssid = row[13].strip()

                    if ssid and ssid.lower() != "<hidden>" and ssid not in seen_ssids:
                        seen_ssids.add(ssid)
                        targets.append({
                            "bssid": bssid,
                            "channel": channel,
                            "ssid": ssid
                        })
                except Exception:
                    continue


    return targets
