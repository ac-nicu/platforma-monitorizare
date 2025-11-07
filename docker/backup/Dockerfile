# Folosim o imagine de bază Python slim
FROM python:3.10-slim

# Setăm directorul de lucru
WORKDIR /app

# Copiem scriptul de backup din directorul 'scripts'
# (presupunând că contextul de build este directorul rădăcină)
COPY scripts/backup.py .

# Nu sunt necesare pachete Python externe (shutil, os, time sunt standard)

# Rulăm scriptul la pornirea containerului
CMD ["python", "backup.py"]