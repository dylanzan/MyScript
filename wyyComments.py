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
import time
import re


class WyyReptile(object):

    url = ''
    filePath = ''
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Cookie': 'nts_mail_user=zsc9602@163.com:-1:1; mail_psc_fingerprint=5ad9e89f6d01b06d4000931415d2947e; _iuqxldmzr_=32; _ntes_nnid=fc752d0b5f3d887efbd891792ff554f4,1548905023326; _ntes_nuid=fc752d0b5f3d887efbd891792ff554f4; WM_TID=qBPZxl7vSjhBVAFBFBMpkZ0D6e7jt2KV; usertrack=CrHubFxVh6tJuSgdA14UAg==; __remember_me=true; P_INFO=zsc9602@163.com|1554033066|0|mail163|00&99|CN&1553910313&cloudmusic#CN&null#10#0#0|178405&0|cloudmusic|zsc9602@163.com; WM_NI=vYDcbUctPVLO9AfJI7h%2BZ4w%2FyDSbuBRswJxiwh3mKaNNOvrY5VczdXAp0FD5aseeQF7cb5Wq2ZRw2oC0T%2B%2BdvF4Il%2BIvNDwvv8IQqY3JgZyTVUgoZb0xof%2FYy5bvQJuaWmU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee89f553bb8aa193b58089968ba3c14e938a9f85ee64b3b39fa4c66badf0fc83c72af0fea7c3b92ab6878c84e15fa1aca0b7cf45fb9faaabcc3dacf596d5f625bb9c9d83f84a92adb9abfb63b5b8fd8eca6b8e928197f153f78aad9be75483b000a7c73fa3adab86d44ef5bdaed6d67bf2869e98b16581f09cccaa70b69afcaaef218baa82a5f67eb6e887b2f453f196a9bbfc60968ba990d96af4a8a187ae53bbebae97d442b7bf998ed837e2a3; JSESSIONID-WYYY=ccnGrqOHOfJxiQoxX6o%2Fqjh0VzfdjWetgHB73XbHV%5CIw79fs2cUV5C2t1OaRS1wUTJ2O%5Cb6HtMbVbykKjWTP01XmYdm%2BEmICwB98yvAPtj79vl%5CdxyRR%2FE7z4TJptwGjzUSdxEwE7XTSBSHiEzeHXgwxRegFR0tE87aBfrN%5C0tA9CmGO%3A1554435339497; MUSIC_U=a0c23480081ce6755d0872c35b14300d5c88a78378f3cf7832d89337a4d414dcc78d05d80ad8e128b865c7f5d98da64131b299d667364ed3; __csrf=9b9e37aa268af132c217ed10eb2b46bd',
               'Host': 'music.163.com',
               'Referer': 'https://music.163.com/',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    def __init__(self, url, filePath):
        self.url = url
        self.filePath = filePath

# 生成16个随机字符
    def generate_random_strs(self, length):
        string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # 控制次数参数i
        i = 0
    # 初始化随机字符串
        random_strs = ""
        while i < length:
            e = random.random() * len(string)
        # 向下取整
            e = math.floor(e)
            random_strs = random_strs + list(string)[e]
            i = i + 1
        return random_strs


# AES加密

    def AESencrypt(self, msg, key):
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

    def RSAencrypt(self, randomstrs, key, f):
        # 随机字符串逆序排列
        string = randomstrs[::-1]
    # 将随机字符串转换成byte类型数据
        text = bytes(string, 'utf-8')
        seckey = int(codecs.encode(text, encoding='hex'),
                     16)**int(key, 16) % int(f, 16)
        return format(seckey, 'x').zfill(256)


# 获取参数

    def get_params(self, page):
        # msg也可以写成msg = {"offset":"页面偏移量=(页数-1) *　20", "limit":"20"},offset和limit这两个参数必须有(js)
        # limit最大值为100,当设为100时,获取第二页时,默认前一页是20个评论,也就是说第二页最新评论有80个,有20个是第一页显示的
        # msg = '{"rid":"R_SO_4_1302938992","offset":"0","total":"True","limit":"100","csrf_token":""}'
        # 偏移量
        offset = (page-1) * 20
    # offset和limit是必选参数,其他参数是可选的,其他参数不影响data数据的生成
        msg = '{"offset":' + str(offset) + \
            ',"total":"True","limit":"20","csrf_token":""}'
        key = '0CoJUm6Qyw8W8jud'
        f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        e = '010001'
        enctext = self.AESencrypt(msg, key)
    # 生成长度为16的随机字符串
        i = self.generate_random_strs(16)

    # 两次AES加密之后得到params的值
        encText = self.AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
        encSecKey = self.RSAencrypt(i, e, f)
        return encText, encSecKey

    # Http链接
    def _getHttpConnection(self, url, data):
        try:
            resp = requests.post(url, headers=self.headers, data=data)
            respContent = resp._content
            if resp.status_code == 200:
                return respContent.decode('UTF-8')
        except Exception as e:
            print('Error: '+e)

    # 如果文件存在，便清除重写，如果不存在，创建，写入
    def _writeFile(self, songName, content):
        localtime = time.strftime('%Y-%m-%d', time.localtime())
        folderPath = str(self.filePath+localtime)
        folder = os.path.exists(folderPath)
        if not folder:
            os.makedirs(folderPath)
            file = str(folderPath+'/'+songName+'.txt')
            if os.path.exists(file):
                with open(file, "a+") as f:
                    f.writelines(str(content))
            else:
                with open(file, "w+") as f:
                    f.writelines(str(content))
        else:
            file = str(folderPath+'/'+songName+'.txt')
            if os.path.exists(file):
                with open(file, "a+") as f:
                    f.writelines(str(content))
            else:
                with open(file, "w+") as f:
                    f.writelines(str(content))

    # 获取歌曲热评
    def _getHotComments(self, content):
        commentsList = []
        paseValue = json.loads(content)
        hotCommentList = list(paseValue['hotComments'])
        for resStr in hotCommentList:
            commentsList.append(resStr['content'])
        return commentsList

   # 获取每日推荐的歌曲列表
    def _getRecommendSongsId(self, pasePageJson):
        songIdDict = {}
        songsJson = json.loads(pasePageJson)
        songsArray = list(songsJson['recommend'])
        for songsInfo in songsArray:
            songIdDict[str(songsInfo['name'])] = songsInfo['id']
        return songIdDict

    def _run(self):
        try:
            page = 1
            params, encSecKey = self.get_params(page)
            data = {'params': params, 'encSecKey': encSecKey}
            songsIdPage = self._getHttpConnection(self.url, data)
            songsIdDict = self._getRecommendSongsId(songsIdPage)
            for k in songsIdDict:
                songUrl = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + \
                    str(songsIdDict[k])+'?csrf_token='
                print(k+'  正在写入……')
                songsComments = self._getHttpConnection(songUrl, data)
                comments = self._getHotComments(songsComments)
                try:
                    for res in comments:
                        self._writeFile(k, str(
                            res+'\n'+'---------------------------------------'+'\n'))
                    print(k+'  已完成')
                except:
                    for res in comments:
                        self._writeFile('ErrorName',str(
                            res+'\n'+'---------------------------------------'+'\n'))
                    print('ErrorName'+'  已完成')
        except Exception as e:
            print('Error: '+e)


if __name__ == "__main__":
    WyyReptile('https://music.163.com/weapi/v2/discovery/recommend/songs?csrf_token=',
               '/media/data/VsCodeProject/songsComments/')._run()
