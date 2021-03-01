import random
import time
import requests
import datetime
from lxml import etree
import json

import re
import urllib.parse
import base64
import hmac
from hashlib import sha1

import config
from util.logmodule import LogModule
from util.proxy import Proxy

logger = LogModule()
proxy = Proxy(logger)

good_moning_time_start = "08:00:00.000"
good_moning_time_end = "08:30:00.000"
good_night_time_start = "23:00:00.000"
good_night_time_end = "23:30:00.000"
good_moning_word = [
    "早安，唔西迪西",
    "早安，玛卡巴卡",
    "早安，小朋友们"
]
good_night_word = [
    "晚安，唔西迪西",
    "晚安，玛卡巴卡",
    "晚安，小朋友们"
]


# 豆瓣的sig算法
def hash_hmac(key, code, sha1):
    hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
    return base64.b64encode(hmac_code).decode()


def get_topic(session, group_id, group_sig_ts):
    # 找到首页最早发出的0回复的帖子，如果没有返回None
    try:
        r = session.get(config.group_topics_url.format(group_id=group_id, sig_ts=group_sig_ts), proxies=proxy.proxy, timeout=5)
        if r.status_code != 200:
            logger.error("Failed to retrieve group topics: " + str(r.status_code))
            proxy.update_proxy()
            return None
        group_json = json.loads(r.text)
        #print(group_json)
        for topic in reversed(group_json["topics"]):
            # print(topic)
            if topic["comments_count"] == 0:
                topic_id = re.findall("\d+", topic["url"])[0]
                return topic_id
        return None
    except Exception as e:
        logger.error("Failed to send request: " + str(e))
        proxy.update_proxy()
        return None


def post_comment(session, topic_id, good_moning_flag, good_night_flag):
    try:
        create_comment_url = config.comment_url_template.format(topic_id=topic_id)
        # 选择一条回复
        now = datetime.datetime.now().strftime('%H:%M:%S.%f')
        comment = random.choice(config.comment_list) # 随机
        if(now > good_moning_time_start and now < good_moning_time_end and good_moning_flag < 3):  # 早安
            comment = good_moning_word[good_moning_flag]
            good_moning_flag +=1
        elif(now > good_night_time_start and now < good_night_time_end and good_night_flag < 3):  # 晚安
            comment = good_night_word[good_night_flag]
            good_night_flag +=1

        timestamp = str(int(time.time()))
        sig = hash_hmac(
            config.client_secret,
            config.sig_code_template.format(topic_id=topic_id, timestamp=timestamp),
            sha1,
        )
        content = config.comment_content_template.format(
            comment=urllib.parse.quote(comment),
            sig=urllib.parse.quote(sig),
            timestamp=timestamp,
        )
        r = session.post(
            create_comment_url, data=content, proxies=proxy.proxy, timeout=5
        )
        #print(json.loads(r.text))
        logger.info(
            "comment: {}, {}, status_code: {}".format(
                comment, create_comment_url, r.status_code
            )
        )
        if r.status_code == 200 or r.status_code == 404:
            return True
        else:
            proxy.update_proxy()
            return False
    except Exception as e:
        logger.error("Failed to send request: " + str(e))
        proxy.update_proxy()
        return False


if __name__ == "__main__":
    good_moning_flag = 0
    good_night_flag = 0

    refresh_count = 0
    reply_count = 0
    continuous_count = 0
    proxy_count = 0
    proxy_threshold = random.randint(50, 80)

    s = requests.Session()
    s.headers.update(config.headers)

    # post_comment(s, 193164655)
    while True:
        now = datetime.datetime.now().strftime('%H:%M:%S.%f')
        if((now > good_night_time_end and now < "24:00:00.000") or (now > "00:00:00.000" and now < good_moning_time_start)):
            good_moning_flag = 0
            good_night_flag = 0
            continue

        group_id = config.group_id_list[refresh_count % 2]  # 按顺序遍历2个小组
        group_sig_ts = config.group_sig_ts_list[refresh_count % 2]

        user_agent = random.choice(config.User_Agent)  # 更新设备信息
        config.headers["User-Agent"] = user_agent
        s.headers.update(config.headers)

        logger.info("第" + str(refresh_count//2) + "次刷新"+group_id+"小组首页")

        topic_id = get_topic(s, group_id, group_sig_ts)
        refresh_count += 1

        if topic_id and post_comment(s, topic_id,good_moning_flag,good_night_flag):
            reply_count += 1
            logger.info("第" + str(reply_count) + "次回复")
            continuous_count += 1
            if continuous_count > 4:
                continuous_count = 0
        else:
            continuous_count = 0

        # 为了避免豆瓣反爬虫机制，连续回复的次数越多，sleep的时间越长
        random_sleep = random.randint(10, 20) + continuous_count * 4
        logger.info("Sleep for " + str(random_sleep) + " seconds")
        time.sleep(random_sleep)

        # 当前的proxy用到一定次数之后，换成一个新的
        proxy_count += 1
        if proxy_count == proxy_threshold:
            proxy.update_proxy()
            proxy_count = 0
            continuous_count = 0
            proxy_threshold = random.randint(50, 80)
