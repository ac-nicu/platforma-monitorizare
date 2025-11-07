# Folosim o imagine de bază Debian/Ubuntu pentru a avea pachetele necesare
FROM ubuntu:22.04

# Evităm prompt-urile interactive în timpul build-ului
ENV DEBIAN_FRONTEND=noninteractive

# Instalăm pachetele necesare pentru monitorizare
# - procps: pentru `ps` și `uptime`
# - coreutils: pentru `df`, `date`, `wc` etc.
# - iproute2: pentru `ss`
# - bash: pentru rularea scriptului
RUN apt-get update && apt-get install -y \
    procps \
    coreutils \
    iproute2 \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Setăm directorul de lucru
WORKDIR /app

# Copiem scriptul de monitorizare din directorul 'scripts'
# (presupunând că contextul de build este directorul rădăcină)
COPY scripts/monitor.sh .

# Facem scriptul executabil
RUN chmod +x monitor.sh

# Rulăm scriptul la pornirea containerului
CMD ["./monitor.sh"]