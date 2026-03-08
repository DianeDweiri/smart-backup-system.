import time
import json
from pathlib import Path
import datetime
import shutil
import logging
import smtplib
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG_FILE = Path("config.json")
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
config = load_config()

SRC_FOLDER = Path(config["source_folder"])
BACKUPS_FOLDER = Path(config["backup_folder"])
LOG_FOLDER = Path(config["log_folder"])

LOG_FOLDER.mkdir(exist_ok=True)
BACKUPS_FOLDER.mkdir(exist_ok=True)

today = datetime.datetime.now().strftime("%Y-%m-%d")
zip_name = BACKUPS_FOLDER / f"backup_{today}.zip"
log_file = LOG_FOLDER / "backup.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

EMAIL = config["email"]

def backup_and_notify():

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    zip_name = BACKUPS_FOLDER / f"backup_{today}"

    message = MIMEMultipart()
    message["From"] = EMAIL["sender"]
    message["To"] = EMAIL["receiver"]
    message["Subject"] = f"Backup System Report - {today}"

    try:
        shutil.make_archive(zip_name.with_suffix(""), 'zip', SRC_FOLDER)
        logging.info("Backup completed successfully")
        body = f"Backup completed successfully for {SRC_FOLDER}"

    except Exception as e:
        logging.error(f"Backup failed: {e}")
        body = f"Backup failed on {SRC_FOLDER}. Error: {e}"

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(EMAIL["smtp_server"], EMAIL["smtp_port"])
        server.starttls()
        server.login(EMAIL["sender"], EMAIL["password"])
        server.sendmail(
            EMAIL["sender"],
            EMAIL["receiver"],
            message.as_string()
        )
        server.quit()

        logging.info("Email sent successfully")

    except Exception as e:
        logging.error(f"Email sending failed: {e}")

schedule.every(config["schedule_days"]).days.do(backup_and_notify)

def run_scheduler():
    logging.info("Backup scheduler started")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    backup_and_notify()
    run_scheduler()