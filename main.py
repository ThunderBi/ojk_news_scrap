import time

import schedule

from health_check import health_check_api
from scrap.ojk_news import *
from logs import *


setup_logger()
call_ojk_news({})
def schedule_ojk_news():
    call_ojk_news({})

def schedule_health_check():
    health_check_api()

schedule.every().day.at("00:00").do(delete_old_files)
schedule.every(5).minutes.do(schedule_ojk_news)
schedule.every(30).seconds.do(schedule_health_check)

while True:
    schedule.run_pending()
    time.sleep(1)  #
