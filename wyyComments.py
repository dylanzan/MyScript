import os
from bs4 import BeautifulSoup
import urllib3
from Crypto.Cipher import AES
from urllib.request import urlopen
import random
import base64
import codecs
import math
import requests
import json

class WyyReptile(object):

    url=''
    filePath=''
    headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Connection': 'keep-alive',
             'Cookie': 'WM_TID=36fj4OhQ7NdU9DhsEbdKFbVmy9tNk1KM; _iuqxldmzr_=32; _ntes_nnid=26fc3120577a92f179a3743269d8d0d9,1536048184013; _ntes_nuid=26fc3120577a92f179a3743269d8d0d9; __utmc=94650624; __utmz=94650624.1536199016.26.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); WM_NI=2Uy%2FbtqzhAuF6WR544z5u96yPa%2BfNHlrtTBCGhkg7oAHeZje7SJiXAoA5YNCbyP6gcJ5NYTs5IAJHQBjiFt561sfsS5Xg%2BvZx1OW9mPzJ49pU7Voono9gXq9H0RpP5HTclE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed5cb8085b2ab83ee7b87ac8c87cb60f78da2dac5439b9ca4b1d621f3e900b4b82af0fea7c3b92af28bb7d0e180b3a6a8a2f84ef6899ed6b740baebbbdab57394bfe587cd44b0aebcb5c14985b8a588b6658398abbbe96ff58d868adb4bad9ffbbacd49a2a7a0d7e6698aeb82bad779f7978fabcb5b82b6a7a7f73ff6efbd87f259f788a9ccf552bcef81b8bc6794a686d5bc7c97e99a90ee66ade7a9b9f4338cf09e91d33f8c8cad8dc837e2a3; JSESSIONID-WYYY=G%5CSvabx1X1F0JTg8HK5Z%2BIATVQdgwh77oo%2BDOXuG2CpwvoKPnNTKOGH91AkCHVdm0t6XKQEEnAFP%2BQ35cF49Y%2BAviwQKVN04%2B6ZbeKc2tNOeeC5vfTZ4Cme%2BwZVk7zGkwHJbfjgp1J9Y30o1fMKHOE5rxyhwQw%2B%5CDH6Md%5CpJZAAh2xkZ%3A1536204296617; __utma=94650624.1052021654.1536048185.1536199016.1536203113.27; __utmb=94650624.12.10.1536203113',
             'Host': 'music.163.com',
             'Referer': 'https://music.163.com/',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    def __init__(self,url,filePath):
        self.url=url
        self.filePath=filePath

# 生成16个随机字符
    def generate_random_strs(self,length):
        string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # 控制次数参数i
        i = 0
    # 初始化随机字符串
        random_strs  = ""
        while i < length:
            e = random.random() * len(string)
        # 向下取整
            e = math.floor(e)
            random_strs = random_strs + list(string)[e] 
            i = i + 1
        return random_strs


# AES加密
    def AESencrypt(self,msg, key):
    # 如果不是16的倍数则进行填充(paddiing)
        padding = 16 - len(msg) % 16
    # 这里使用padding对应的单字符进行填充
        msg = msg + padding * chr(padding)
    # 用来加密或者解密的初始向量(必须是16位)
        iv = '0102030405060708'
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
    # 加密后得到的是bytes类型的数据
        encryptedbytes = cipher.encrypt(msg)
    # 使用Base64进行编码,返回byte字符串
        encodestrs = base64.b64encode(encryptedbytes)
    # 对byte字符串按utf-8进行解码
        enctext = encodestrs.decode('utf-8')

        return enctext


# RSA加密
    def RSAencrypt(self,randomstrs, key, f):
    # 随机字符串逆序排列
        string = randomstrs[::-1]
    # 将随机字符串转换成byte类型数据
        text = bytes(string, 'utf-8')
        seckey = int(codecs.encode(text, encoding='hex'), 16)**int(key, 16) % int(f, 16)
        return format(seckey, 'x').zfill(256)


# 获取参数
    def get_params(self,page):
    # msg也可以写成msg = {"offset":"页面偏移量=(页数-1) *　20", "limit":"20"},offset和limit这两个参数必须有(js)
    # limit最大值为100,当设为100时,获取第二页时,默认前一页是20个评论,也就是说第二页最新评论有80个,有20个是第一页显示的
    # msg = '{"rid":"R_SO_4_1302938992","offset":"0","total":"True","limit":"100","csrf_token":""}'
    # 偏移量
        offset = (page-1) * 20
    # offset和limit是必选参数,其他参数是可选的,其他参数不影响data数据的生成
        msg = '{"offset":' + str(offset) + ',"total":"True","limit":"20","csrf_token":""}'
        key = '0CoJUm6Qyw8W8jud'
        f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        e = '010001'
        enctext =self.AESencrypt(msg, key)
    # 生成长度为16的随机字符串
        i = self.generate_random_strs(16)

    # 两次AES加密之后得到params的值
        encText = self.AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
        encSecKey = self.RSAencrypt(i, e, f)
        return encText, encSecKey

    def _getHtml(self,url,data):
        try:
            resp=requests.post(self.url,headers=self.headers,data=data)
            respContent=resp._content
            if resp.status_code==200:
                return respContent.decode('UTF-8')
        except Exception as e:
            print('Error: '+e)

    # def _paseMusicUrl(self,tag):
    #     reqs=requests.session()
    #     musicPage=reqs.get(self.url,headers=self.headers)._content
    #     print(musicPage.decode('UTF-8'))
    #     soup=BeautifulSoup(musicPage,'html.parser')
    #     links=soup.find_all(tag)
    #     for link in links:
    #         print(link)
    #     return links

    def _writeFile(self,content):
        with open(self.filePath,"a") as f:
            f.writelines(str(content))

    def _getHotComments(self,content):
        commentsList=[]
        paseValue=json.loads(content)
        hotCommentList=list(paseValue['hotComments'])
        for resStr in hotCommentList:
            commentsList.append(resStr['content'])
        return commentsList

    def _run(self):
        page=1
        params,encSecKey=self.get_params(page)
        data={'params':params,'encSecKey':encSecKey}
        resp=self._getHtml(self.url,data)
        print(resp)
        comments=self._getHotComments(resp)
        for res in comments:
            self._writeFile(str(res+'\n'+'---------------------------------------'+'\n'))

if __name__ == "__main__":
   WyyReptile('https://music.163.com/weapi/v1/resource/comments/R_SO_4_514761281?csrf_token=','/media/data/VsCodeProject/a.txt')._run()
   
