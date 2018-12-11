import base64
import os

import requests

'''
@author ClouderDC
@date 20181210
'''

class GetGfwFile(object):
    url="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"

#检测网络连通性
    def _CheckNetwork(seft):
        testVal=os.popen("ping 114.114.114.114 -c 1").readlines()
        try:
            packetsLoss=testVal[4].split()
            if packetsLoss[5]=="0%":
                returnVal="True"
                return returnVal
        except:
            print("Network Error")
            returnVal="False"
            return returnVal


#解析gfwlist编码
    def _Base64Analysis(seft,url):
        try:
            res=requests.get(seft.url)
            resBase64=res.text
            resValue=base64.b64decode(resBase64)
            return str(resValue,encoding="utf-8")
        except:
            print("Analysis Error!")

#指定路径创建pac文件
    def _WriteFile(seft,filePath):
        try:
            getListFileValues=seft._Base64Analysis(seft.url)
            if os.path.exists(filePath)==True:#如果存在，先删除再创建
                os.remove(filePath)
                with open(filePath,"a+") as f:
                    f.writelines(getListFileValues) #将解析结果写入指定文件
                    if(os.path.exists(filePath))==True:
                        print("Create success,plz check your create file:     "+filePath)
                    else:
                        print("Create file failure")
            else:
                with open(filePath, "a+") as f:
                    f.writelines(getListFileValues)
                    if (os.path.exists(filePath)) == True:
                        print("Create success,plz check your create file:     " + filePath)
                    else:
                        print("Create file failure")
        except:
            print("File Write Error!")

#执行
    def  run(seft):
        if seft._CheckNetwork()!="False":
            print("运行此脚本请保证脚本的运行权限，并保证能联通互联网的情况下；请给需要创建的文件指定绝对路径，如没有指定路径，便在本脚本所在目录下创建。望您知晓")
            filePath = input("请输入文件路径：")
            seft._WriteFile(filePath)

if __name__ == '__main__':
    getGfwFile=GetGfwFile()
    getGfwFile.run()



