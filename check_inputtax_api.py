# coding:utf-8
# author:water
import requests
import json
import ssl
import base64


ssl._create_default_https_context = ssl._create_unverified_context
http_url ="https://*******.action"
data_json = {"appcode":"12345678",
            "data":{
                    "nsrsbh":"91110000710927388B",
                    "fpdm":"011001900111",
                    "fphm":"46104392",
                    "kprq":"20190523",
                    "je":"45.10",
                    "jym":"761193"

                    }
            }
p = requests.post(http_url, json=data_json,verify =  False)
p_dict = json.loads(p.text) #json解析响应文本
#或者jsonstr = response.json()
print(p.status_code)
return_msg = p_dict['returnStateInfo']['returnMessage']
print(return_msg)
datas = str(base64.b64decode(p_dict["data"]),"utf-8")
print(datas)



