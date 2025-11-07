import os
import time
import shutil
import logging
from datetime import datetime

# --- Configurare ---

# Preluarea variabilelor de mediu cu valori implicite
try:
    # Convertim intervalul la un număr întreg
    BACKUP_INTERVAL_SEC = int(os.environ.get('BACKUP_INTERVAL', '5'))
except ValueError:
    logging.warning("BACKUP_INTERVAL invalid. Folosind valoarea implicită de 5 secunde.")
    BACKUP_INTERVAL_SEC = 5

BACKUP_DIR = os.environ.get('BACKUP_DIR', '/app/backup') # Calea DINTRE container
SOURCE_FILE_PATH = os.environ.get('SOURCE_FILE', '/app/data/system-state.log')

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler()] # Loghează la stdout
)

def ensure_dir_exists(dir_path):
    """Asigură existența unui director."""
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logging.info(f"Directorul '{dir_path}' a fost creat.")
    except PermissionError:
        logging.error(f"Eroare de permisiune: Nu se poate crea directorul '{dir_path}'.")
        return False
    except Exception as e:
        logging.error(f"Eroare la crearea directorului '{dir_path}': {e}")
        return False
    return True

def get_file_mtime(file_path):
    """Returnează timestamp-ul de modificare al fișierului sau None."""
    try:
        if os.path.exists(file_path):
            return os.path.getmtime(file_path)
    except FileNotFoundError:
        logging.warning(f"Fișierul sursă '{file_path}' nu a fost încă găsit.")
    except Exception as e:
        logging.error(f"Eroare la accesarea fișierului sursă '{file_path}': {e}")
    return None

def perform_backup(last_mtime):
    """Verifică și efectuează backup-ul dacă fișierul s-a modificat."""
    
    current_mtime = get_file_mtime(SOURCE_FILE_PATH)
    
    if current_mtime is None:
        # Fișierul sursă nu există sau nu este accesibil
        return last_mtime 

    # Verifică dacă fișierul s-a modificat
    if current_mtime != last_mtime:
        logging.info(f"Detectat modificare în '{SOURCE_FILE_PATH}'. Se inițiază backup-ul.")
        
        # Asigură existența directorului de backup
        if not ensure_dir_exists(BACKUP_DIR):
            return last_mtime # Nu se poate continua fără directorul de backup

        try:
            # Construiește numele fișierului de backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"system-state_backup_{timestamp}.log"
            destination_path = os.path.join(BACKUP_DIR, backup_filename)
            
            # Copiază fișierul
            shutil.copy2(SOURCE_FILE_PATH, destination_path)
            
            logging.info(f"Backup creat cu succes: '{destination_path}'")
            return current_mtime # Actualizează mtime
            
        except PermissionError:
            logging.error(f"Eroare de permisiune: Nu se poate scrie în '{destination_path}'.")
        except IOError as e:
            logging.error(f"Eroare I/O la copierea fișierului: {e}")
        except Exception as e:
            logging.error(f"Eroare neașteptată la efectuarea backup-ului: {e}")
            
    else:
        logging.info("Fișierul nu s-a modificat. Nu este necesar backup.")
        
    return last_mtime # Returnează mtime-ul vechi dacă nu s-a făcut backup

def main():
    logging.info("Scriptul de backup a pornit.")
    logging.info(f"Director backup: {BACKUP_DIR}")
    logging.info(f"Fișier sursă: {SOURCE_FILE_PATH}")
    logging.info(f"Interval verificare: {BACKUP_INTERVAL_SEC} secunde")
    
    last_modification_time = None # Inițializăm cu None pentru a forța un prim backup

    while True:
        try:
            last_modification_time = perform_backup(last_modification_time)
            time.sleep(BACKUP_INTERVAL_SEC)
        except KeyboardInterrupt:
            logging.info("Script de backup oprit manual.")
            break
        except Exception as e:
            # Prinde orice altă eroare care ar putea opri bucla principală
            logging.critical(f"Eroare critică în bucla principală: {e}. Se repornește bucla...")
            time.sleep(BACKUP_INTERVAL_SEC) # Așteaptă înainte de a reîncerca

if __name__ == "__main__":
    main()