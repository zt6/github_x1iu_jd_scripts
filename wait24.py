import time
import datetime
import logging

while datetime.datetime.now().hour != 16:
    logging.warn(f'{datetime.datetime.now()}未到时间')
    time.sleep(5)
