#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
import requests
import os , subprocess
import time
import tkinter
import os.path
import tkinter.messagebox
from bs4 import BeautifulSoup
import threading

# 获取Windows平台临时文件夹
path = os.getenv('temp')
filename = os.path.join(path, 'info.txt')
# 创建应用程序窗口
root = tkinter.Tk()
# 在窗口上创建标签组件
#wifi
root.title('自动连接')
root.geometry("%sx%s+%d+%d" % ('250','170',(root.winfo_screenwidth()-250) / 2,(root.winfo_screenheight()-400) / 2))
root.resizable(width=False,height=False)

labelName = tkinter.Label(root,text='学号：',justify=tkinter.RIGHT,width=80)
labelName.place(x=30, y=25, width=80, height=20)
# 创建字符串变量和文本框组件，同时设置关联的变量
varName = tkinter.StringVar(root, value='')
entryName = tkinter.Entry(root,width=80,textvariable=varName)
entryName.place(x=110, y=25, width=80, height=20)

labelPwd  = tkinter.Label(root,text='密码：',justify=tkinter.RIGHT,width=80)
labelPwd.place(x=30, y=50, width=80, height=20)
# 创建密码文本框
varPwd = tkinter.StringVar(root, value='')
entryPwd = tkinter.Entry(root,show='*',width=80,textvariable=varPwd)
entryPwd.place(x=110, y=50, width=80, height=20)
#创建连接进度条
Loding = tkinter.StringVar()
labelLoding = tkinter.Label(root,textvariable=Loding)
labelLoding.place(x=10, y=130, width=80, height=20)
Loding.set('等待连接...')
# 尝试自动填写用户名和密码
name = ''
pwd = ''
ip = "http://172.16.30.33/"
try:
   with open(filename) as fp:
       n, p = fp.read().strip().split(',')
       varName.set(n)
       varPwd.set(p)
       name = entryName.get()
       pwd = entryPwd.get()
except:
   pass
post_addr = ip
post_header = {
   'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
   'Accept-Encoding': 'gzip, deflate',
   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',  
   'Connection': 'keep-alive',
   'DNT': '1',
   'Host': '172.16.30.33',
   'Referer': 'http://172.16.30.33/a79.htm?isReback=1',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.30 Safari/537.36 Edg/84.0.522.11',
   'X-Requested-With': 'XMLHttpRequest',
}
post_data = {
   'callback': 'dr1591477287421',
   'DDDDD': '182017070',
   'upass': '08232010',
   '0MKKey': '123456',
   'R1': '0',
   'R3': '1',
   'R6': '0',
   'para': '00',
   '_':'1591477259645',  
}
   
def SingleLoginBotton():
    try:
        with open(filename, 'w') as fp:
           name = entryName.get()
           pwd = entryPwd.get()
           fp.write(','.join((name,pwd)))
        Loding.set('正在连接...')
        SingleLogin("http://172.16.30.33/")       
    except:
        pass  
buttonOk = tkinter.Button(root,
text='单次连接',
command=SingleLoginBotton)
buttonOk.place(x=20, y=100, width=60, height=20)

def SingleLogin(ip):
        print(ip)
        i=0    
        while True:
           print(ip)
           if i>=1:
               if ip=="http://172.16.30.45/":   
                   SingleLogin("http://172.16.30.33/") 
               else: SingleLogin("http://172.16.30.45/")       
           b=requests.get(ip)
           if(b.status_code==200):
               b_bsObj = BeautifulSoup(b.text, 'html.parser')
               baidu_input = b_bsObj.find_all("title")
               #print(baidu_input)
               if str(baidu_input) == "[<title>注销页</title>]":                  
                   Loding.set('连接成功') 
                   #print(i)
                   sys.exit(0)
               else:
                   requests.post(post_addr, data=post_data, headers=post_header) 
                   i+=1  
           else:
               top = tkinter.Tk()
               top.withdraw()
               top.update()
               tkinter.messagebox.showinfo('提醒', '未检测到校园网，请检查网线/WIFI')  
               top.destroy()       
               sys.exit(0)
def MultipleLogonBotton():
    with open(filename, 'w') as fp:
        name = entryName.get()
        pwd = entryPwd.get()
        fp.write(','.join((name,pwd)))
    root.destroy()
    while True:
        MultipleLogon("http://172.16.30.33/")          
buttonOk = tkinter.Button(root,
text='防断连接',
command=MultipleLogonBotton)
buttonOk.place(x=95, y=100, width=60, height=20)
def MultipleLogon(ip): 
    i=0          
    while True:
        print(ip)
        if i>=1:
            #top = tkinter.Tk()
            #op.withdraw()
            #top.update()
            #tkinter.messagebox.showinfo('提醒', '连接超时，正在切换ip重连')  
            #top.destroy()
            if ip=="http://172.16.30.45/":   
               MultipleLogon("http://172.16.30.33/") 
            else: MultipleLogon("http://172.16.30.45/")
        b=requests.get(ip)
        if(b.status_code==200):
            b_bsObj = BeautifulSoup(b.text, 'html.parser')
            baidu_input = b_bsObj.find_all("title")
            #print(baidu_input)
            if str(baidu_input) != "[<title>注销页</title>]":
                requests.post(post_addr, data=post_data, headers=post_header)
                i+=1
                continue
            else:i=0
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
#清空用户输入的用户名和密码
   varName.set('')
   varPwd.set('')
buttonCancel = tkinter.Button(root,
text='清除输入',command=cancel)
buttonCancel.place(x=170, y=100, width=60, height=20)
if __name__=="__main__":
    try:
        #启动消息循环
        root.mainloop() 
    except Exception as e:
        print ('[ERROR]:'),
        print (e)

