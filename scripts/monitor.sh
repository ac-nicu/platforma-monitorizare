#!/bin/bash

# Setează calea fișierului de log.
# Îl vom plasa într-un director /app/data care va fi un volum partajat.
LOG_FILE="/app/data/system-state.log"

# Preluarea intervalului din variabila de mediu, cu valoare implicită de 5 secunde.
MONITOR_INTERVAL=${MONITOR_INTERVAL:-5}

echo "Scriptul de monitorizare a pornit. Se va scrie în $LOG_FILE la fiecare $MONITOR_INTERVAL secunde."

# Buclă infinită pentru a rula monitorizarea
while true; do
    # Folosim > pentru a suprascrie fișierul la fiecare rulare
    {
        echo "--- System State Snapshot: $(date) ---"
        echo ""
        
        echo ">>> Hostname:"
        hostname
        echo ""
        
        echo ">>> System Uptime & Load:"
        uptime
        echo ""
        
        echo ">>> CPU Usage (top 5 processes):"
        # Afișează un instantaneu din top, în modul batch
        ps -eo pcpu,pid,user,args --sort=-pcpu | head -n 6
        echo ""
        
        echo ">>> Memory Usage:"
        free -h
        echo ""
        
        echo ">>> Disk Usage (Root Filesystem):"
        df -h /
        echo ""
        
        echo ">>> Active Processes Count:"
        echo "Total Tasks: $(ps -e | wc -l)"
        echo ""
        
        echo ">>> Network Connections (Listening):"
        ss -tuln
        echo ""
        
        echo "--- End of Snapshot ---"
        
    } > "$LOG_FILE" # Redirecționarea suprascrie fișierul

    # Așteaptă intervalul specificat
    sleep "$MONITOR_INTERVAL"
done