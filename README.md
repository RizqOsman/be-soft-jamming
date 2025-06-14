# 📡 Soft Jamming API - FastAPI

> A RESTful API for WiFi soft jamming using FastAPI.  
> Designed to simplify scanning, jamming, interface management, and activity logging using multiple Alfa Network RTL8814AU interfaces.

---

## 📦 Main Features

- 🔍 WiFi Scanning (SSID, BSSID, Channel)
- 🛰 Auto & Manual Client Scanning (with progress)
- ⚔️ WiFi Jamming (auth flood, deauth, beacon spam, hcxjamming)
- 🧠 Dynamic Multi-interface RTL8814AU Support (8 units or more)
- 🧩 Per-interface Jamming Control (`/jammer/stop?iface=...`)
- 🧼 Monitor Mode Auto-Setup on Startup
- 📝 SQLite Activity Logging (via `logs.db`)
- 🧰 Modular FastAPI Router Structure

---

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RizqOsman/be-soft-jamming.git 
cd be-soft-jamming
```

### 2. Create a Virtual Environment
Activate it depending on your OS:

- Linux / macOS:
```bash
source venv/bin/activate
```

- Windows (PowerShell/CMD):
```bash
venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### ▶ Run the Application 
⚠️ Requires sudo to access wireless interfaces
```bash
sudo uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 🔀 Folder Structure (Summary)
```bash
be-soft-jamming
├── README.md
├── app
│   ├── __pycache__
│   │   └── main.cpython-312.pyc
│   ├── database
│   │   ├── db_init.py
│   │   ├── logger.py
│   │   └── logs.db
│   ├── main.py
│   ├── models
│   │   └── schema.py
│   ├── routers
│   │   ├── attack.py
│   │   ├── crack.py
│   │   ├── handshake.py
│   │   ├── interface.py
│   │   ├── jammer.py
│   │   ├── logger.py
│   │   ├── phising.py
│   │   └── scan.py
│   └── services
│       ├── attacker.py
│       ├── cracker.py
│       ├── handshake.py
│       ├── interface.py
│       ├── jammer.py
│       ├── logger.py
│       ├── scanner.py
│       └── utils.py
├── app.log
├── logs.db
├── requirements.txt
├── scan_results.json
├── ssids.txt
├── start.sh
├── stop.sh
```

### 📦 Install `btlejack`
```bash
git clone https://github.com/virtualabs/btlejack.git
cd btlejack
sudo pip install .
```

⚙️ Supported Tools & Dependencies
Make sure the following tools are installed on your system:
1) aircrack-ng suite:

- ✅ airodump-ng

- ✅ aireplay-ng

2) ✅ mdk4

3) ✅ hcxjamming

4) ✅ python3, pip, uvicorn, fastapi, rich, sqlite3


📡 API Overview

| Endpoint           | Method | Description                           |
| ------------------ | ------ | ------------------------------------- |
| `/scan/interfaces` | GET    | List RTL8814AU interfaces & modes     |
| `/scan/ssid`       | GET    | Timed SSID scan (`iface`, `duration`) |
| `/scan/start/scan` | POST   | Start live scanning                   |
| `/scan/stop/scan`  | POST   | Stop and get scan results             |
| `/scan/status`     | GET    | Get scan progress + metadata          |

⚔️ Jamming

| Endpoint                 | Method | Description                          |
| ------------------------ | ------ | ------------------------------------ |
| `/attack/deauth`         | POST   | Deauth specific targets              |
| `/attack/jam/multi`      | POST   | Start jamming with N interfaces      |
| `/jammer/status`         | GET    | List active jamming interfaces       |
| `/jammer/stop?iface=...` | POST   | Stop jamming on a specific interface |

Interface Management
| Endpoint             | Method | Description                          |
| -------------------- | ------ | ------------------------------------ |
| `/interface/summary` | GET    | Get all RTL8814AU status & modes     |
| `/interface/roles`   | GET    | Get current interface role map       |
| `/interface/roles`   | POST   | Update interface roles (JSON format) |
| `/interface/setup`   | POST   | Auto-activate monitor mode           |
---