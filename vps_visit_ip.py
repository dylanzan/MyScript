import json
import requests
import urllib3
import time

urllib3.disable_warnings()
host = 'https://dm-81.data.aliyun.com/rest/160601/ip/getIpInfo.json?ip='
appcode = '079f5054a1064a0c9811b2ac875c7a84'
headers={}
headers['Authorization']='APPCODE ' + appcode

ips_1=[]
with open('/media/data/ip.txt') as f:
    for line in f.readlines():
        ips_1.append(line.strip('\n'))
ips_2 = list(set(ips_1))
print(ips_2)


def ip_address_check(ip):
    res=requests.get(url=host+ip,headers=headers,verify=False).json()
    print(res['data']['ip'],res['data']['country'],res['data']['city'],res['data']['isp'])

for i in range(0, ips_2.__len__()):
   if i/100 in range(1,10):
       time.sleep(10)
       #print('sleeping')
       ip_address_check(ips_2[i])
   else:
       ip_address_check(ips_2[i])