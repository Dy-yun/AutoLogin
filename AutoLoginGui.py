#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
import requests
import os
import subprocess
import time
import tkinter
import tkinter.messagebox
from bs4 import BeautifulSoup
import threading

# 获取Windows平台临时文件夹
path = os.getenv('temp')
filename = os.path.join(path, 'info.txt')
# 创建应用程序窗口
root = tkinter.Tk()
# 在窗口上创建标签组件
# wifi
root.title('自动连接')
root.geometry("%sx%s+%d+%d" % ('250', '170', (root.winfo_screenwidth() -
              250) / 2, (root.winfo_screenheight()-400) / 2))
root.resizable(width=False, height=False)


labelName = tkinter.Label(root, text='学号：', justify=tkinter.RIGHT, width=80)
labelName.place(x=30, y=25, width=80, height=20)
# 创建字符串变量和文本框组件，同时设置关联的变量
varName = tkinter.StringVar(root, value='')
entryName = tkinter.Entry(root, width=80, textvariable=varName)
entryName.place(x=110, y=25, width=80, height=20)

labelPwd = tkinter.Label(root, text='密码：', justify=tkinter.RIGHT, width=80)
labelPwd.place(x=30, y=50, width=80, height=20)
# 创建密码文本框
varPwd = tkinter.StringVar(root, value='')
entryPwd = tkinter.Entry(root, show='*', width=80, textvariable=varPwd)
entryPwd.place(x=110, y=50, width=80, height=20)
# 创建连接进度条
Loding = tkinter.StringVar()
labelLoding = tkinter.Label(root, textvariable=Loding)
labelLoding.place(x=10, y=130, width=80, height=20)
Loding.set('等待连接...')
# 尝试自动填写用户名和密码
name = ''
pwd = ''

try:
    with open(filename) as fp:
        n, p = fp.read().strip().split(',')
        varName.set(n)
        varPwd.set(p)
        name = entryName.get()
        pwd = entryPwd.get()
except:
    pass

ip1 = "http://172.16.30.33/"
ip2 = "http://172.16.30.45/"
post_data = {
    'DDDDD': name,
    'upass': pwd,
    '0MKKey': '123456',
    'R3': '1'
}


def singleLoginBotton():
    try:
        with open(filename, 'w') as fp:
            name = entryName.get()
            pwd = entryPwd.get()
            fp.write(','.join((name, pwd)))
        Loding.set('正在连接...')
        singleLogin(ip1)
    except:
        pass


buttonOk = tkinter.Button(root,
                          text='单次连接',
                          command=singleLoginBotton)
buttonOk.place(x=20, y=100, width=60, height=20)


# 单次连接方法
def singleLogin(post_ip):
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
                Loding.set('连接成功')
                sys.exit(0)
        else:
            top = tkinter.Tk()
            top.withdraw()
            top.update()
            tkinter.messagebox.showinfo('提醒', '未检测到校园网，请检查网线/WIFI')
            top.destroy()
            sys.exit(0)


def multipleLoginBotton():
    with open(filename, 'w') as fp:
        name = entryName.get()
        pwd = entryPwd.get()
        fp.write(','.join((name, pwd)))
    root.destroy()
    while True:
        multipleLogin(ip1)


buttonOk = tkinter.Button(root,
                          text='防断连接',
                          command=multipleLoginBotton)
buttonOk.place(x=95, y=100, width=60, height=20)


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
                print("ip切换至%s" % (post_ip))
                continue
            else:
                # print("正在与"+post_ip+"通讯中...")
                time.sleep(5)
                # os.system('cls')
                i = 0
        else:
            top = tkinter.Tk()
            top.withdraw()
            top.update()
            tkinter.messagebox.showinfo('提醒', '未检测到校园网，请检查网线/WIFI')
            top.destroy()
            sys.exit(0)
    return False
# 取消按钮的事件处理函数


def cancel():
    # 清空用户输入的用户名和密码
    varName.set('')
    varPwd.set('')


buttonCancel = tkinter.Button(root, text='清除输入', command=cancel)
buttonCancel.place(x=170, y=100, width=60, height=20)
if __name__ == "__main__":
    try:
        # 启动消息循环
        root.mainloop()
    except Exception as e:
        print('[ERROR]:'),
        print(e)
