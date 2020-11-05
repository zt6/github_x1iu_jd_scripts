import time
import datetime

while datetime.datetime.now().hour != 16:
    print(datetime.datetime.now(), '未到达预定时间')
    time.sleep(5)
