#!/bin/bash
cd "$(dirname "$0")"

while true; do
    clear
    echo "========================================================"
    echo "       YUKI WATCHDOG - PERSISTENT MODE"
    echo "========================================================"
    echo ""

    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        echo "Virtual environment not found, trying with global python..."
    fi

    echo "Starting Yuki Watchdog (Process Monitor)..."
    echo "[Press Ctrl+C to stop the monitoring loop]"
    echo ""

    python3 yuki_watchdog.py

    echo ""
    echo "========================================================"
    echo "Watchdog process ended. Restarting in 5 seconds..."
    echo "========================================================"
    sleep 5
done
