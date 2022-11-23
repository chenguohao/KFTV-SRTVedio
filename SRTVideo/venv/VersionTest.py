
import os
import shutil
import zipfile
import time
import json
class BaseResource:
    vBaseUrl = []
    vExUrl = []

class FileResource(BaseResource):
    version=""

def obj_dict(obj):
    return obj.__dict__
fileRes = FileResource()
fileRes.version = "1.2"
fileRes.vBaseUrl = ["http://www.baidu.com","http://www.sina.com"]

fileRes2 = FileResource()
fileRes2.version = "2.2"
fileRes2.vBaseUrl = ["http://www.baidu.com","http://www.sina.com"]

resList = [fileRes , fileRes2]

str = json.dumps(resList,default=obj_dict)

print(str)