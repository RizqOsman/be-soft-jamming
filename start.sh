#!/bin/bash

LOG_FILE="app.log"

echo "📡 Memulai FastAPI WiFi Toolkit API..."
source venv/bin/activate

# Jalankan aplikasi di background dan log output ke app.log
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > "$LOG_FILE" 2>&1 &


echo "✅ Aplikasi berjalan di latar belakang. Log tersedia di: $LOG_FILE"
echo "📌 Proses ID disimpan di 'api.pid'"
