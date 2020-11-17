import time
import datetime
import logging
import sys 
import random

padding = 1
if len(sys.argv) == 2:
    padding = int(sys.argv[1])

target_time = datetime.datetime.now()
target_time = target_time.replace(minute=59, second=60-padding-1, microsecond=500000)

while datetime.datetime.now() < target_time:
    logging.warn(f'{datetime.datetime.now()}未到{target_time}点')
    time.sleep(0.1)

time.sleep(random.random())
