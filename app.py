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
IMAGES_FOLDER = "Images"
IMAGE_NAME = "sample.png"  # You can change this to the image you want to send
IMAGE_PATH = os.path.join(IMAGES_FOLDER, IMAGE_NAME)


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
            logger.info(f"Loaded message from {message_path}: {message}")
            return message
    except FileNotFoundError:
        logger.error(f"Message file not found: {message_path}")
    except Exception as e:
        logger.error(f"Error reading message file: {e}")
    return None


def warmup_whatsapp_web(phone):
    try:
        logger.info(f"Warming up WhatsApp Web for {phone}...")
        pywhatkit.sendwhatmsg_instantly(phone, "", wait_time=15, tab_close=False)
        logger.info("WhatsApp Web loaded and ready.")
        time.sleep(10)  # Give extra time for WhatsApp Web to fully load
    except Exception as e:
        logger.error(f"Warm-up failed: {e}")


def send_whatsapp_image_and_text(phone, image_path, message):
    try:
        logger.info(f"Sending image to {phone} with caption...")
        pywhatkit.sendwhats_image(phone, image_path, caption=message, tab_close=False)
        logger.info(f"Image and text sent to {phone}")
        time.sleep(8)  # Wait to avoid spamming and allow WhatsApp to process
    except Exception as e:
        logger.error(f"Failed to send image and text to {phone}: {e}")


def main():
    contacts = read_contacts(CONTACTS_CSV)
    message = read_message(MESSAGE_FILE)
    if not contacts:
        logger.warning("No contacts to send messages to.")
        return
    if not message:
        logger.warning("No message to send.")
        return
    # Warm up WhatsApp Web for the first contact
    first_phone = contacts[0]['phone']
    if first_phone.startswith('+'):
        warmup_whatsapp_web(first_phone)
    else:
        logger.warning(f"Phone number for {contacts[0]['name']} is not in international format: {first_phone}")
    # Now send image and text to all contacts
    for contact in contacts:
        phone = contact['phone']
        if not phone.startswith('+'):
            logger.warning(f"Phone number for {contact['name']} is not in international format: {phone}")
            continue
        send_whatsapp_image_and_text(phone, IMAGE_PATH, message)

if __name__ == "__main__":
    main()
