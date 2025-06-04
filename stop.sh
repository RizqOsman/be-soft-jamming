#!/bin/bash

echo "🛑 Menghentikan semua proses terkait..."

# Kill uvicorn
pkill -f "uvicorn"

# Kill tools yang mungkin aktif
sudo pkill airodump-ng
sudo pkill mdk4
sudo pkill hostapd
sudo pkill dnsmasq
sudo pkill aireplay-ng

echo "✅ Semua proses dihentikan."
