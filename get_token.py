import os
import requests
import json

OS_AUTH_URL = 'http://192.168.100.128'
body={ 'auth': { 'identity': { 'methods': ['password'],'password': {'user': {'domain': {'name': 'default'},'name': 'admin', 'password': 'admin'} } }, 'scope': { 'project': { 'domain': { 'name': '''default''' }, 'name':  'admin' } } }}
headers={}
headers['Content-Type'] = 'application/json'
headers['Accept'] = '*/*'

def get_token():
    get_token_url=OS_AUTH_URL+':35357/v3/auth/tokens'
    result=requests.post(get_token_url,headers=headers,data=json.dumps(body)).headers['X-Subject-Token']
    return result

def user_list():
    user_list_url=OS_AUTH_URL+':35357/v3/users'
    headers['X-Auth-Token']=get_token()
    result=requests.get(user_list_url,headers=headers).json()
    print(headers)
    print(result)

def images_list():
    images_list_url=OS_AUTH_URL+':9292/v2/images'
    headers['X-Auth-Token']=get_token()
    result=requests.get(images_list_url,headers=headers).json()
    print(headers)
    print(result)

user_list()