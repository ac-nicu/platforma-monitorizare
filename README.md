# Platforma de Monitorizare a Starii unui Sistem

## Scopul Proiectului

Obiectivul principal al proiectului este de a crea un sistem de monitorizare de baza, robust si scalabil, aplicand cunostintele dobandite in timpul cursului de DevOps, pentru a demonstra intelegerea modului in care tehnologiile diferite lucreaza impreuna. Avem astfel partea de scripturi (folosind Bash si Python), containerizarea (folosind Docker), orchestrare (folosind Kubernetes), provizionare (folosind Ansible).

## Structura Proiectului

Proiectul contine fisierul README.md (fiind acesta) cu detalii despre proiect (structura, continut, mod de rulare etc.) si urmatoarele directoare principale:

- `/scripts`: contine scriptul de shell **monitor.sh** (partea de generare informatii despre sistem) si scriptul de python **backup.py** (partea de backup al fisierului log generat de scriptul shell);
- `/docker`: contine doua subdirectoare (**monitor** si **backup**) pentru fisierele Dockerfile ce contin comenzile necesare pentru crearea imaginilor de docker; in radacina directorului avem docker-compose.yml ce ruleaza cele doua containere;
- `/ansible`: contine un director playbooks pentru cele doua playbooks, unul care instaleaza Docker si Docker Compose si unul care face deploy fisierelor necesare si porneste aplicatia folosind docker compose up; in radacina directorului avem fisierul ini pentru a defini unde sa provizioneze acestea;
- `/k8s`: contine manifestele deployment.yaml (ce defineste namespace, pods si volumes pentru containere) si hpa.yaml care reprezinta autoscalerul.

## Setup si Rulare

Pentru a ne putea folosi de acest proiect, urmati urmatorii pasi de clonare a acestuia intr-un repository tip Empty din GitHub:

```bash
git clone git@github.com:ac-nicu/platforma-monitorizare.git
cd platforma-monitorizare
git remote -v
git remote remove origin
git remote add origin git@github.com:<USERUL_VOSTRU>/platforma-monitorizare.git
git branch -M main
git push -u origin main
```


