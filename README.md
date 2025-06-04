# 📡 Soft Jamming API - FastAPI

> A RESTful API for WiFi soft jamming using FastAPI.  
> Designed to simplify scanning, jamming, logging, and future support for handshake capture and deauthentication attacks using multiple interfaces.

---

## 📦 Main Features

- 🔍 WiFi Network Scanning (airodump-ng)
- ⚠️ Signal Jamming (auth, deauth, beacon, hcxjamming)
- 🧠 Multi-interface RTL8814AU support (min. 2 at once)
- 📑 Activity Logging to SQLite Database
- 📂 Modular FastAPI router structure
- 🛠 Interface Monitor Mode Activation

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

### 🧪 Dependencies (Core Tools)
- airodump-ng

- aireplay-ng

- mdk4

- hcxjamming

- rich (console output), sqlite3, uvicorn, fastapi
---