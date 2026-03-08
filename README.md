Smart Backup System 💾

A Python automation tool that automatically creates compressed backups of important folders, logs the process, and sends an email notification with the result.

This project demonstrates automation, scheduling, logging, configuration management, and email integration in Python.

Features

• Automatic folder backup
• Creates ZIP archives of important files
• Daily logging system to track backups and errors
• Email notifications after backup completion
• Configurable settings using a JSON config file
• Automatic scheduled execution using a task scheduler
• Error handling to ensure the system keeps running

Configuration

All settings are stored in config.json
Example:

{
  "source_folder": "C:/Users/User/Documents/ImportantFiles",
  "backup_folder": "C:/Users/User/Backups",
  "log_folder": "logs",

  "schedule_days": 1,

  "email": {
    "sender": "your_email@gmail.com",
    "receiver": "receiver_email@gmail.com",
    "password": "your_app_password",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  }
}

How It Works?

1. The script loads settings from config.json.

2. The selected folder is compressed into a ZIP backup.

3. The backup is saved with the current date.

4. The system logs the operation in backup.log.

5. An email notification is sent with the backup status.

6. The system runs automatically based on the defined schedule.

Example Log Output
2026-03-08 10:20:03 - INFO - Backup completed successfully
2026-03-08 10:20:05 - INFO - Email sent successfully

If something fails:
2026-03-08 10:20:03 - ERROR - Backup failed: [Error message]

Installation
1. Clone the repository
git clone https://github.com/DianeDweiri/smart-backup-system.git
cd smart-backup-system
2. Install dependencies
pip install schedule
Running the System

Start the backup scheduler:

python backup.py

The script will:

• Run an immediate backup
• Continue running in the background
• Execute backups based on the configured schedule

Technologies Used

Python
Pathlib
Logging
Shutil
SMTP (Email Automation)
Schedule Library

Learning Goals

This project demonstrates practical automation concepts:

File system automation

Task scheduling

Error handling

Logging systems

Email automation

Configurable Python applications

Future Improvements

Possible upgrades:

• Automatic deletion of old backups
• Backup encryption
• Cloud storage integration (Google Drive / AWS S3)
• Email attachments with backup reports
• Docker deployment

Author

AI & Data Science student passionate about automation, AI, and intelligent systems.