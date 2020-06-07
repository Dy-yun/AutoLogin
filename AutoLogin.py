#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import os , subprocess
from bs4 import BeautifulSoup
ip = "http://172.16.30.33/"
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
   'DDDDD': '这里输入你的账号',
   'upass': '这里输入你的密码',
   '0MKKey': '123456',
   'R1': '0',
   'R3': '1',
   'R6': '0',
   'para': '00',
   '_':'1591477259645',  
}
def MultipleLogon(ip): 
    i=0          
    while True:
        print(ip)
        if i>=1:
            if ip=="http://172.16.30.45/":   
               MultipleLogon("http://172.16.30.33/") 
            else: MultipleLogon("http://172.16.30.45/")
        b=requests.get(ip)
        if(b.status_code==200):
            b_bsObj = BeautifulSoup(b.text, 'html.parser')
            baidu_input = b_bsObj.find_all("title")
            if str(baidu_input) != "[<title>注销页</title>]":
               requests.post(post_addr, data=post_data, headers=post_header)
               i+=1
               continue
            else:
                i=0                    
    return False
if __name__=="__main__":
    try:
        MultipleLogon("http://172.16.30.33/")
    except Exception as e:
        print ('[ERROR]:'),
        print (e)
