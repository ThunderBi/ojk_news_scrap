import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def setup_logger():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    handler = TimedRotatingFileHandler(
        "logs/app.log",
        when="midnight",
        interval=1,
        backupCount=3
    )
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    handler.suffix = "%Y%m%d"

    # Add handler to root logger
    logging.getLogger().addHandler(handler)

def delete_old_files():
    log_directory = "logs"
    days_to_keep = 3
    now = datetime.now().hour
    cutoff = now - (days_to_keep * 24)

    for filename in os.listdir(log_directory):
        file_path = os.path.join(log_directory, filename)

        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)

            if file_mtime < cutoff:
                os.remove(file_path)