import time,datetime,shutil,logging,smtplib,schedule,json
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


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

def handle_file(path):
    file = Path(path)

    if not file.exists() or not file.is_file():
        return

    for folder, extensions in config["file_types"].items():
        if file.suffix.lower() in extensions:

            dest = Path(config["destination_folder"]) / folder
            dest.mkdir(parents=True, exist_ok=True)

            dest_file = dest / file.name

            counter = 1
            while dest_file.exists():
                dest_file = dest / f"{file.stem}_{counter}{file.suffix}"
                counter += 1

            try:
                shutil.move(str(file), str(dest_file))
                logging.info(f"{file.name} moved to {folder}")
            except Exception as e:
                logging.error(f"{file.name} failed: {e}")

            break

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

class WatchHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(2)
            handle_file(event.src_path)

schedule.every(config["schedule_days"]).days.do(backup_and_notify)

if __name__ == "__main__":
    observer = Observer()
    event_handler = WatchHandler()

    observer.schedule(event_handler, path=str(SRC_FOLDER), recursive=False)
    observer.start()
    try:
        while True:
            schedule.run_pending()
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
