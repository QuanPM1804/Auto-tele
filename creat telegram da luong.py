import os, json, time, requests, shutil, asyncio, threading, datetime, sqlite3, subprocess
from threading import Thread
from functools import partial
from datetime import datetime
import numpy as np
import pathlib
import shutil
import time
from datetime import datetime
import sympy
from py_essentials import simpleRandom as sr
import shutil
import base64
import re
import uiautomator2
import subprocess
from uiautomator2 import Device
import  os, json
from faker import Faker
import pyperclip
import requests
import sys
import random
from pyrogram import Client
# from telethon.sync import TelegramClient
# from opentele.api import API
from urllib.request import urlopen
from telethon import TelegramClient, events, sync,connection, functions, types
from telethon import functions, types
from telethon.errors.rpcerrorlist import *
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
# from telethon.sync import TelegramClient




CREATE_NO_WINDOW = 0x08000000


#SYSTEM VAR, PLEASE DONT CHANGE
debug_mode = False

#CONFIG VAR, CAN BE CHANGE
# max_thread  = 2 # <----- Số luồng tối đa chạy đồng thời


folder_acc= 'Account done'
password = ''

email =''
code_mail=''
username=''
host =''
port =''
# TAO_ACC_XIT=''
# LOI_DANG_KI=''




list_key_tinsoft = ['']


proc = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
serviceList = proc.communicate()[0].decode('ascii').split('\n')
# print(proc)
print(serviceList)
list_serial = []

for i in range(1, len(serviceList) -2 ):
    try:
        device1 = serviceList[i].split('\t')[0]

        
        # if len(device1) < 20 :
        # print(len(device1))
        list_serial.append(device1)
        print(device1)
    except Exception as e:
        print(str(e))
        pass
print(list_serial) 
# time.sleep(1000)
if len(list_serial) < 1:
            print('Không tìm thấy thiết bị nào')
            sys.exit()
max_thread = len(list_serial)





async def chia_luong():
    global luot_dang_chay, current_index, luong_hien_tai
    so_lan_can_chay = 16
    current_index = 0
    luot_dang_chay = 0
    for luot_hien_tai in range(so_lan_can_chay):
        try:
            for luong_hien_tai in range(max_thread):
                # print(f'==> luong hien tai {luong_hien_tai}')

                while True:
                    if luot_dang_chay < max_thread:
                        # if luot_dang_chay < len(list_serial):
                        luot_dang_chay += 1
                        print(f'Lượt hiện tại: {luot_hien_tai} ---> luồng hiện tại:{luong_hien_tai} | index = {current_index} ---> số luồng đang chạy đồng thời : {luot_dang_chay}')
                    
                        x = threading.Thread(target = call_session_work, args = (current_index,))

                        x.start()
                        await asyncio.sleep(0.1)
                        break
                    else:
                        await asyncio.sleep(0.1)
                
                # if current_index < len(list_serial):
                current_index += 1

                #     os.system('pause')

        except Exception as e:
            if 'list index out of range' in str(e):
                # print("ĐÃ CHẠY HẾT SỐ LUỒNG CẦN CHẠY RỒI!")
                pass


def call_session_work(current_index): 
    try:   
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())   
        # print('1')   
        asyncio.run(session_work(current_index,list_key_tinsoft))
        # print('2')
    except Exception as e:
        print(f'Lỗi khi call_session_work {e}')


async def get_new_tinsoft(key_tinsoft,ten_thiet_bi, luong_hien_tai):
    # global host, port


    print(key_tinsoft)
    # time.sleep(10000)
    a = f'http://proxy.tinsoftsv.com/api/changeProxy.php?key={key_tinsoft}&location=0'
    # res = requests.get(a)
    res = urlopen(a)
    result = res.read()
    b = (json.loads(result))
    is_success = b['success']
    # print(is_success)

    if is_success == True:
        proxy = (b['proxy'])
        # print(proxy)
        doi_ip = f'adb -s "{ten_thiet_bi}" shell settings put global http_proxy {proxy}'
        
        # print(doi_ip)
        # os.system(doi_ip)
        # return proxy
        host, port = proxy.split(':')
        print(host,port)
        return  host, port
    else:
        next_change = b['next_change']
        for nc in range(next_change+7):
            print(f'{key_tinsoft}\nWait {next_change+6-nc}s for next change', 1.5)
            # print(f'Wait {next_change+6-nc}s to get new proxy')
            time.sleep(1)
        a = f'http://proxy.tinsoftsv.com/api/changeProxy.php?key={key_tinsoft}&location=0'
        # res = requests.get(a)
        res = urlopen(a)
        result = res.read()
        b = (json.loads(result))
        # print(b)
        is_success = b['success']
        if is_success == True:
            proxy = (b['proxy'])
            # print(proxy)
            host, port = proxy.split(':')
            print(host,port)
            
            doi_ip = f'adb -s "{ten_thiet_bi}" shell settings put global http_proxy {proxy}'
            return  host, port
            print(doi_ip)
            os.system(doi_ip)
        else:
            return False

async def open_proxy (device, host, port):
    # global host,port
    try:
        # print(f'1{host}')
        LOI_DANG_KI = False
        device.app_stop_all()
        # device.app_clear('org.telegram.messenger')
        device.app_clear('com.scheler.superproxy')
        
        device.app_start('com.scheler.superproxy', use_monkey= True)
        device.xpath ('//android.widget.Button[@index = "2"]').click_exists(timeout =5)
        device.xpath ('//android.widget.Button[@index = "2"]').click_exists(timeout =1)

        device.xpath ('//android.widget.EditText[@index = "1"]').click_exists(timeout =2)
        # print(f'aaa{host}')
        device.send_keys(host)
        device.xpath ('//android.widget.EditText[@index = "2"]').click_exists(timeout =2)
        # print(port)
        device.send_keys(port)
        await asyncio.sleep(1)
        device.xpath ('//android.widget.Button[@index = "1"]').click_exists(timeout =2)   
        device.xpath ('//android.widget.Button[@content-desc = "Start"]').click_exists(timeout =2)  
        device.xpath ('//android.widget.Button[@content-desc = "Start"]').click_exists(timeout =1)
        await asyncio.sleep(1)
        if device.xpath("//android.widget.Button[contains(@content-desc, 'Stop')]").exists:
            print('Da doi proxy')
        else:
            LOI_DANG_KI = True
            return LOI_DANG_KI
    except Exception as e:
        print(str(e))
        pass


async def creat_telegram_1(device, phone_number):
    LOI_DANG_KI = False
    OTP_GET_DONE = False
    device.app_clear('org.telegram.messenger')
    fake = Faker()
    name = fake.name()
    device.app_start('org.telegram.messenger', use_monkey= True)
    time.sleep(2)
    device.xpath('//android.widget.TextView[@index ="5"]').click(timeout =3)

    # viotp
    # for i in range(5):
    #     link_creat=  f'https://api.viotp.com/request/getv2?token=dbea2b6eeb724835b515d04403a1af2b&serviceId=19'
    #     get_sdt = requests.get(link_creat)
    #     json_get_sdt=json.loads(get_sdt.text)
    #     phone_number = json_get_sdt['data']['phone_number']
    #     request_id = json_get_sdt['data']['request_id']
    #     if phone_number.isdecimal() == True:
    #         break
    #     time.sleep(1)

    # ironsim
    for i in range(10):
        link_creat=  f'https://ironsim.com/api/phone/new-session?token=drjeaoyw6vlqy258g2hy2ih1wgbht5f5&service=19'
        get_sdt = requests.get(link_creat, timeout = 3)
        json_get_sdt=json.loads(get_sdt.text)
        phone_number = json_get_sdt['data']['phone_number']
        request_id = json_get_sdt['data']['session']
        if phone_number.isdecimal() == True:
            break
        time.sleep(1)
    print (phone_number)
    if phone_number.isdecimal() == False:
        LOI_DANG_KI = True
        return LOI_DANG_KI
        
    # print (request_id)
    device.xpath('//android.widget.EditText[@index= "0"]').click_exists(timeout =1)
    time.sleep(1)
    device.xpath('//android.view.View[@index= "7"]').click(timeout =2)
    time.sleep(1)
    device.xpath('//android.view.View[@index= "3"]').click(timeout =1)
    time.sleep(1)
    device.xpath('//android.widget.EditText[@content-desc = "Phone number"]').click (timeout = 1)
    time.sleep(1)
    device.send_keys(phone_number)
    time.sleep(1)
    device.click(925, 1310)
    time.sleep(2)

    

    if device(text="Too many").exists(timeout =3) == True:
        try:
            link_refund = f'https://ironsim.com/api/session/cancel?token=drjeaoyw6vlqy258g2hy2ih1wgbht5f5&session={request_id}'
            refund = requests.get(link_refund)
            json_refund=json.loads(refund.text)
            print(json_refund)
        except:
            pass
        return
    
    
        

    try:
        device.xpath('//android.widget.TextView[@text= "Yes"]').click(timeout = 3)
            
    except:
        pass



    
    # time.sleep(2)

    #viotp
    # for i in range(5):
    #     link_code=  f'https://api.viotp.com/session/getv2?requestId={request_id}&token=dbea2b6eeb724835b515d04403a1af2b'
    #     get_code = requests.get(link_code)
    #     json_get_code=json.loads(get_code.text)
    #     code = json_get_sdt['data']['Code']
    #     if code.isdecimal() == True:
    #         break
    #     time.sleep(1)
    if device(text="Enter code").exists(timeout =30) == True:

        for i in range(10):
            link_code=  f'https://ironsim.com/api/session/{request_id}/get-otp?token=drjeaoyw6vlqy258g2hy2ih1wgbht5f5'
            print(link_code)
            get_code = requests.get(link_code)
            json_get_code=json.loads(get_code.text)
            print(json_get_code)
            code = ''
            if json_get_code["data"]["status"] == 0:

                code = json_get_code["data"]["messages"][0]["otp"]

                print(code)
                if code.isdecimal() == True:
                    OTP_GET_DONE =True
                    # print(f'11{code}')
                    break
            time.sleep(5)
        if OTP_GET_DONE == False:
            try:
                link_refund = f'https://ironsim.com/api/session/cancel?token=drjeaoyw6vlqy258g2hy2ih1wgbht5f5&session={request_id}'
                refund = requests.get(link_refund)
                json_refund=json.loads(refund.text)
                print(json_refund)
            except:
                pass
            return
        device.send_keys(code)

        if device(text="Enter your name and add a profile picture.").exists(timeout =10) == True:
            device.send_keys(name)
            device.click(926, 1880)
            device.xpath('//android.widget.TextView[@text= "Not now"]').click_exists(timeout = 7)
            # await asyn
            return phone_number
        
        return phone_number
    
async def creat_session_telethon(device, phone_number):
    if '+84' not in phone_number:
        phone_number = f'+84{phone_number}'

    # api = API.TelegramAndroid.Generate()
    # api_id = api.api_id
    # api_hash = api.api_hash
    api_id = 6
    api_hash = 'eb06d4abfb49dc3eeb1aeb98ae0f581e'

    device_telethon = random.choice(['Lenovo','Realme','Xiaomi','Samsung','Vivo','BPhone','Nokia','Asus','Huawei','Oppo','Sony','HTC','LG','Phillips','Sky'])
    a_1=random.randint(1,10)
    a_2=random.randint(1,10)
    a_3=random.randint(1,10)
    a_4=random.randint(1,10)
    a_5=random.randint(1,10)
    device_telethon_done = f'{device_telethon} {a_1}{a_2}{a_3}'
    random_app_version = f'{a_1}.{a_2}.{a_3}.{a_4}.{a_5}'

    if not os.path.exists(f'{folder_acc}/{phone_number}/Telethon') : os.makedirs(f'{folder_acc}/{phone_number}/Telethon')

    client = TelegramClient(f'{folder_acc}/{phone_number}/Telethon/{phone_number}', api_id, api_hash, device_model= device_telethon_done, system_version = device_telethon,  app_version = random_app_version, lang_code = "en")
    print(phone_number)
    await client.connect()
    phone_number_hash = await client.send_code_request (f'{phone_number}')
    device.xpath('//android.view.ViewGroup[@index= "0"]').click_exists(timeout = 15)
    receive = device.xpath('//android.view.ViewGroup[@index= "0"]').get_text()
    split1 = receive.split(': ')[1]
    login_code = split1.split('. Do')[0]
    print (login_code)
    await client.sign_in(phone_number_hash, login_code)
    time.sleep(0.5)
    await client.send_message('me','me')   
    



        # print (code)
        
        # time.sleep(5)

# def open_tele():
#     from opentele.api import API
#     api = API.


async def session_work(current_index, list_key_tinsoft):
    global  list_used ,list_wallet, device1, list_serial, TAO_ACC_XIT
    try:

        ten_thiet_bi = list_serial[luong_hien_tai-1]

        device =  Device(ten_thiet_bi)
        try:
            device.unlock()
        except:
            pass

       

        key_tinsoft = ''
        key_tinsoft = list_key_tinsoft[luong_hien_tai-1]

        phone_number = '+84585523896'


        api_id = 6
        api_hash = 'eb06d4abfb49dc3eeb1aeb98ae0f581e'

        device_telethon = random.choice(['Lenovo','Realme','Xiaomi','Samsung','Vivo','BPhone','Nokia','Asus','Huawei','Oppo','Sony','HTC','LG','Phillips','Sky'])
        a_1=random.randint(1,10)
        a_2=random.randint(1,10)
        a_3=random.randint(1,10)
        a_4=random.randint(1,10)
        a_5=random.randint(1,10)
        device_telethon_done = f'{device_telethon} {a_1}{a_2}{a_3}'
        random_app_version = f'{a_1}.{a_2}.{a_3}.{a_4}.{a_5}'

        
        client = TelegramClient(f'{phone_number}', api_id, api_hash, device_model= device_telethon_done, system_version = device_telethon,  app_version = random_app_version, lang_code = "en")
        print(phone_number)
        await client.connect()
        phone_number_hash = await client.send_code_request (f'{phone_number}')
        device.xpath('//android.view.ViewGroup[@index= "0"]').click_exists(timeout = 15)
        receive = device.xpath('//android.view.ViewGroup[@index= "3"]').get_text()
        split1 = receive.split(': ')[1]
        login_code = split1.split('. Do')[0]
        print (login_code)
        await client.sign_in(phone_number_hash, login_code)
        time.sleep(0.5)
        await client.send_message('me','me')

        print('11111')



        time.sleep(10000)


        for i in range(1000000):
      
            TAO_ACC_XIT = False
            LOI_DANG_KI =False

            host, port = await get_new_tinsoft(key_tinsoft, ten_thiet_bi, luong_hien_tai)
            


            # # global key_tinsoft
            
            await open_proxy(device, host, port)

            time.sleep(1)


            phone_number = await creat_telegram_1(device, phone_number)
            print(phone_number)
            time.sleep(1)

            if phone_number == None or LOI_DANG_KI == True or phone_number == True:
                continue

            if phone_number != None :
                if phone_number.isdecimal() == True:
                
                    await creat_session_telethon(device, phone_number)
            
            
            await asyncio.sleep(1000)


    except Exception as e:
        print(e)
    # print('1')









asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  
asyncio.run(chia_luong()) 
