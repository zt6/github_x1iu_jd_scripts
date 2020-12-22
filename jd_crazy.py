import requests
import time
import os
import datetime
import logging
from threading import Thread
import random


class CrazyJoy:
    JD_API_HOST = 'https://api.m.jd.com'

    def __init__(self, cookie):
        self.cookie = cookie
        self.needs_stop = False
        self.joy_list = None
        self.top_level = None
        self.get_joy_list()

    def do_task(self, function_id, body=None, delay=5):
        if body is None:
            body = dict()

        time.sleep(delay)

        url = f'{CrazyJoy.JD_API_HOST}/?body={str(body)}&appid=crazy_joy&functionId={function_id}&t={int(time.time()*1000)}&uts=b8bf8319bc0e120e166849cb7e957d335fe01979'
        headers = {
        'Cookie': self.cookie,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'jdpingou;iPhone;3.15.2;14.2;ae75259f6ca8378672006fc41079cd8c90c53be8;network/wifi;model/iPhone10,2;appBuild/100365;ADID/00000000-0000-0000-0000-000000000000;supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/0;hasOCPay/0;supportBestPay/0;session/158;pap/JA2015_311210;brand/apple;supportJDSHWK/1;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://crazy-joy.jd.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        }
        
        return requests.get(url, headers=headers).json()

    def move_or_merge(self, origin, to):
        function_id = 'crazyJoy_joy_moveOrMerge'
        body = {
        "operateType": "MERGE",
        "fromBoxIndex": origin,
        "targetBoxIndex": to
        }
        result = self.do_task(function_id, body)
        logging.warning(result)
    
    def get_joy_list(self):
        function_id = 'crazyJoy_user_gameState'
        body = {
        'paramData': {
            # 'inviter': 'Lwc_OhLLBZSOt1Uc2gay6g=='
            'inviter': ''
            }
        }
        result = self.do_task(function_id, body)
        # print(result)
        self.joy_list = result['data']['joyIds']
        self.top_level = result['data']['userTopLevelJoyId']

    def sell_joy(self,joyId, boxId): # joyId:joy等级 boxId:joy位置
        body = {"action": "SELL", "joyId": joyId, "boxId": boxId}
        result = self.do_task('crazyJoy_joy_trade', body)

    def buy_joy(self, joy_level):
        body = {"action": "BUY", "joyId": joy_level, "boxId": ""}
        result = self.do_task('crazyJoy_joy_trade', body)

        if result['data'].get('lackCoin', False):
            return False

        return result['success']

    def produce(self):
        return self.do_task('crazyJoy_joy_produce', delay=random.random()+4)

    def upgrade(self):
        self.get_joy_list()
        sorted_joy_list = sorted(self.joy_list)
        for item in sorted_joy_list:
            if item != 0:
                break
        lowest_level = item

        if sorted_joy_list[0] == 0: # 有空位
            if lowest_level > self.top_level - 4:
                if self.buy_joy(self.top_level - 4):
                    return
                else:
                    time.sleep(300)
            if not self.buy_joy(lowest_level):
                time.sleep(300)
            self.merge_all()

        else:
            self.sell_joy(lowest_level, self.joy_list.index(lowest_level))

    def merge_all(self):
        while True:
            self.get_joy_list()
            seen = []
            for to, level in enumerate(self.joy_list):
                if level == 0:
                    continue
                if level not in seen:
                    seen.append(level)
                else:
                    origin = self.joy_list.index(level)
                    logging.warning(f'joy_list:{self.joy_list} from:{origin} to:{to}')
                    self.move_or_merge(origin, to)
                    break
            else:
                break

    def make_money(self):
        while True:
            time.sleep(2)
            self.get_joy_list()
            print(self.joy_list)
            seen = []
            for to, level in enumerate(self.joy_list):
                if level not in seen:
                    seen.append(level)
                else:
                    origin = seen.index(level)
                    self.move_or_merge(origin, to)
                    break
            else:
                break


def produce_main(crazy_joy):
    while not crazy_joy.needs_stop:
        try:
            produce_result = crazy_joy.produce()
            logging.warning(f"获得：{produce_result['data']['coins']}  余额：{produce_result['data']['totalCoinAmount']}")
        except:
            time.sleep(5)


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    cookie = os.environ['JD_COOKIE'].split('\n')[0]
    crazy_joy = CrazyJoy(cookie)
    produce_thread = Thread(target=produce_main, args=(crazy_joy,))
    produce_thread.start()

    crazy_joy.merge_all()
    while (datetime.datetime.now() - start_time).total_seconds() < 60*60:
        try:
            crazy_joy.upgrade()
        except:
            time.sleep(30)

    crazy_joy.needs_stop = True
