import csv
import pywhatkit
import logging
from colorama import init, Fore, Style
import time
import os

# Initialize colorama
init(autoreset=True)

# Set up logging with color codes
class ColorFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: Fore.CYAN + "[DEBUG] %(message)s" + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + "[INFO] %(message)s" + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + "[WARNING] %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "[ERROR] %(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Fore.MAGENTA + "[CRITICAL] %(message)s" + Style.RESET_ALL,
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter())
file_handler = logging.FileHandler("automation.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger = logging.getLogger("whatsapp_automation")
logger.setLevel(logging.DEBUG)
logger.handlers = []  # Remove any existing handlers
logger.addHandler(handler)
logger.addHandler(file_handler)

CONTACTS_CSV = os.path.join("uploads", "contacts.csv")
MESSAGE_FILE = os.path.join("message", "send.txt")


def read_contacts(csv_path):
    contacts = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get('Name')
                phone = row.get('Phone')
                if not phone:
                    logger.warning(f"Missing phone for contact: {name}")
                    continue
                contacts.append({'name': name, 'phone': phone})
        logger.info(f"Loaded {len(contacts)} contacts from {csv_path}")
    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_path}")
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
    return contacts


def read_message(message_path):
    try:
        with open(message_path, 'r', encoding='utf-8') as f:
            message = f.read().strip()
            if not message:
                logger.warning(f"Message file {message_path} is empty.")
                return None
            logger.info(f"Loaded message from {message_path}")
            return message
    except FileNotFoundError:
        logger.error(f"Message file not found: {message_path}")
    except Exception as e:
        logger.error(f"Error reading message file: {e}")
    return None


def send_whatsapp_message(phone, message):
    try:
        logger.info(f"Sending message to {phone}...")
        pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)
        logger.info(f"Message sent to {phone}")
        time.sleep(5)  # Wait to avoid spamming
    except Exception as e:
        logger.error(f"Failed to send message to {phone}: {e}")


def main():
    contacts = read_contacts(CONTACTS_CSV)
    message = read_message(MESSAGE_FILE)
    if not contacts:
        logger.warning("No contacts to send messages to.")
        return
    if not message:
        logger.warning("No message to send.")
        return
    for contact in contacts:
        phone = contact['phone']
        # Ensure phone number is in correct format (e.g., '+1234567890')
        if not phone.startswith('+'):
            logger.warning(f"Phone number for {contact['name']} is not in international format: {phone}")
            continue
        send_whatsapp_message(phone, message)

if __name__ == "__main__":
    main()
