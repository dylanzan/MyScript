import urllib3
import requests

class job(object):
    
    url=''
    filePath=''

    def __init__(self,url,filePath):
        self.url=url
        self.filePath=filePath

    def _getHtml(self):
        http=urllib3.PoolManager()
        resp=http.request('get',self.url).data
        return resp.decode('UTF-8')

    def _writeFile(self,context):
        with open(self.filePath,'w+') as f:
            f.writelines(context)
    
    def _run(self):
        res=self._getHtml()
        self._writeFile(res)

if __name__ == '__main__':
    job('https://sou.zhaopin.com/?jl=489&kw=%E4%BA%91%E8%AE%A1%E7%AE%97&kt=3','/media/data/text.txt')._run()
    