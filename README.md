# WhatsApp Automation with pywhatkit

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features
- Send WhatsApp messages to a list of contacts from a CSV file
- Message content is loaded from a text file (`message/send.txt`)
- Robust error handling and logging (console + file)
- Colorized logs in the console using `colorama`
- Easy to configure and extend

## Project Structure
```
├── app.py                # Main automation script
├── requirements.txt      # Python dependencies
├── automation.log        # Log file (auto-generated)
├── uploads/
│   └── contacts.csv      # Contacts CSV (Name, Phone)
├── message/
│   └── send.txt          # Message to send
```

## Prerequisites
- Python 3.8+
- Google Chrome browser (required by pywhatkit)
- WhatsApp Web account (logged in on Chrome)

## Setup Instructions

1. **Clone the repository**
   ```cmd
   git clone <your-repo-url>
   cd py-whatsapp
   ```

2. **Create and activate a virtual environment (optional but recommended)**
   ```cmd
   python -m venv gui-env
   gui-env\Scripts\activate
   ```

3. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Prepare your contacts CSV**
   - Place your contacts in `uploads/contacts.csv` with columns: `Name`, `Phone` (phone numbers in international format, e.g., `+1234567890`).

5. **Write your message**
   - Edit `message/send.txt` and write the message you want to send.

6. **Run the automation**
   ```cmd
   python app.py
   ```
   - The script will open WhatsApp Web in Chrome and send the message to each contact.
   - All logs will be shown in the console and saved to `automation.log`.

## Notes
- Make sure you are logged into WhatsApp Web in Chrome before running the script.
- The script waits a few seconds between messages to avoid spamming.
- Only phone numbers in international format (starting with `+`) will be processed.

## Troubleshooting
- If you encounter issues with Chrome or WhatsApp Web, ensure Chrome is installed and up to date.
- Check `automation.log` for detailed error messages.

## License
This project is for educational and personal automation use only.
