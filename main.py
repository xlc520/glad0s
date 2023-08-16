#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import requests
import base64

COOKIE = os.environ["COOKIE"]
cookies = COOKIE.split('\n')
PUSHPLUS_TOKEN = os.environ["PUSHPLUS_TOKEN"]
session = requests.session()
c = "aHR0cHM6Ly9nbGFkb3Mucm9ja3MvYXBpL3VzZXIvY2hlY2tpbg=="
s = "aHR0cHM6Ly9nbGFkb3Mucm9ja3MvYXBpL3VzZXIvc3RhdHVz"
r = "aHR0cHM6Ly9nbGFkb3Mucm9ja3MvY29uc29sZS9jaGVja2lu"
o = "aHR0cHM6Ly9nbGFkb3Mucm9ja3M="
title = "R2xhRE9T562+5Yiw6YCa55+l"
token = "Z2xhZG9zLm9uZQ=="
ua = "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk1LjAuNDYzOC42OSBTYWZhcmkvNTM3LjM2"


def base64_decode(encode_data):
    decode_data = base64.b64decode(encode_data).decode('utf-8')
    return decode_data


def pushplus_bot(title, content):
    try:
        if not PUSHPLUS_TOKEN:
            print("PUSHPLUS服务的token未设置!!\n取消推送")
            return
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSHPLUS_TOKEN,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)


def checkin(cookie):
    payload = {"token": base64_decode(token)}
    head1 = {
        'cookie': cookie,
        'referer': base64_decode(r),
        'origin': base64_decode(o),
        'user-agent': base64_decode(ua),
        'content-type': 'application/json;charset=UTF-8'
    }
    head2 = {
        'cookie': cookie,
        'referer': base64_decode(r),
        'origin': base64_decode(o),
        'user-agent': base64_decode(ua)
    }
    try:
        checkin = session.post(base64_decode(c), headers=head1, data=json.dumps(payload))
        state = session.get(base64_decode(s), headers=head2)
    except Exception as e:
        print(f"失败1：{e}")
        return None, None, None
    try:
        msg = checkin.json()['message']
        mail = state.json()['data']['email']
        time = state.json()['data']['leftDays'].split('.')[0]
    except Exception as e:
        print(f"失败2：{e}")
        return None, None, None
    return msg, mail, time


def main():
    contents = []
    if not cookies:
        return ""
    for cookie in cookies:
        msg, mail, time = checkin(cookie)
        content = "结果:" + str(msg) + "\n剩余天数：" + str(time) + "\n账号：" + str(mail) + "\n"
        contents.append(content)
    contents_str = "".join(contents)
    pushplus_bot(base64_decode(title), contents_str)


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
