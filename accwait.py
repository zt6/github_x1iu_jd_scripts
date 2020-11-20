import time
import datetime
import logging
import sys 
import random

padding = 1 # 提前时间
interval = 1 # 区间

if len(sys.argv) >= 2:
    padding = float(sys.argv[1])
if len(sys.argv) == 3:
    interval = float(sys.argv[2])

start_time = 60 - padding - 0.5*interval
second_setting = int(start_time)
ms_setting = int((start_time - second_setting)*10**6)

target_time = datetime.datetime.now()

if target_time.minute > 30:
    target_time = target_time.replace(minute=59, second=second_setting, microsecond=ms_setting)

    i=0
    while datetime.datetime.now() < target_time:
        i += 1
        if i % 30 == 0:
            logging.warn(f'{datetime.datetime.now()}未到{target_time}点')
        time.sleep(0.03)

    time.sleep(random.random()*interval)
