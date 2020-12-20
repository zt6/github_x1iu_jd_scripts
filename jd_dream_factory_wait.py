import requests
import time
import os
import random

if __name__ == "__main__":
    time.sleep(600)

    JD_API_HOST = 'https://m.jingxi.com'
    function_id = 'userinfo/GetUserInfo'
    body = 'pin=&sharePin=&shareType=&materialTuanPin=&materialTuanId='
    cookie = os.environ['JD_COOKIE'].split('\n')[0]
    headers = {
      'Cookie': cookie,
      'Host': 'm.jingxi.com',
      'Accept': '*/*',
      'Connection': 'keep-alive',
      'User-Agent': 'jdpingou;iPhone;3.14.4;14.0;ae75259f6ca8378672006fc41079cd8c90c53be8;network/wifi;model/iPhone10,2;appBuild/100351;ADID/00000000-0000-0000-0000-000000000000;supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/1;hasOCPay/0;supportBestPay/0;session/62;pap/JA2015_311210;brand/apple;supportJDSHWK/1;Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
      'Accept-Language': 'zh-cn',
      'Referer': 'https://wqsd.jd.com/pingou/dream_factory/index.html',
      'Accept-Encoding': 'gzip, deflate, br',
    }
    url = f'{JD_API_HOST}/dreamfactory/{function_id}?zone=dream_factory&{body}&sceneval=2&g_login_type=1&_time={int(time.time()*1000)}&_={int(time.time()*1000)}'

    try:
        get_ret = requests.get(url, headers=headers).json()
        level = get_ret['data']['user']['currentLevel']
    except:
        time.sleep(80*60)
        exit(0)

    wait_minutes = 35 + 5 * level
    time.sleep(wait_minutes*60)
    time.sleep(random.randint(15, 45))



