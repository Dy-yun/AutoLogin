#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import time
import os
from bs4 import BeautifulSoup
ip1 = "http://172.16.30.33/"
ip2 = "http://172.16.30.45/"
post_data = {
    # 账户
    'DDDDD': '这里输入账户',
    # 密码
    'upass': '这里输入密码',
    # 运营商选择
    '0MKKey': '123456',
    'R3': '1'
}


def multipleLogin(post_ip):
    i = 0
    while True:

        baidu = requests.get("http://www.baidu.com/")
        nfu = requests.get(post_ip)
        if(baidu.status_code + nfu.status_code == 400):
            baidu_title = BeautifulSoup(
                baidu.text, 'html.parser').find_all("title")
            nfu_title = BeautifulSoup(
                nfu.text, 'html.parser').find_all("title")
            if (str(baidu_title) == str(nfu_title) == "[<title>上网登录页</title>]"):
                requests.post(post_ip, data=post_data)
                i += 1
                # print("正在第%d次重连至%s" % (i, post_ip))
                time.sleep(2)
                continue
            # 通网ip更改后也随之更改
            elif ((str(baidu_title) == "[<title>上网登录页</title>]") & (str(nfu_title) == "[<title>注销页</title>]")):
                if(post_ip == ip1):
                    post_ip = ip2
                else:
                    post_ip = ip1
                # print("ip切换至%s" % (post_ip))
                continue
            else:
                # print("正在与"+post_ip+"通讯中...")
                time.sleep(5)
                # os.system('cls')
                i = 0
        else:
            print("网络未连接")


if __name__ == "__main__":
    try:
        multipleLogin(ip1)

    except Exception as e:
        print('[ERROR]:'),
        print(e)
