import base64
import json
import urllib
from utils import decorator
from urllib import request
import os


@decorator
def get_token(host):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json; charset=UTF-8"}
    req = request.Request(url=host, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    res_json = json.loads(res.decode('utf-8'))
    return res_json["access_token"]


'''
进行post请求
url：请求地址
value：请求体
'''


@decorator
def get_info_post_json_data(url, value):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    req = request.Request(url=url, data=value, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    return res.decode('utf-8')


'''
调用百度API，进行人脸探测
imgPath：图片的地址
access_token：开发者token
'''


@decorator
def get_baidu_face_tech(img_path, access_token):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    # 图片转换为base64
    img = base64.b64encode(f.read())
    f.close()
    params = {"face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,race,quality", "image": img,
              "image_type": "BASE64", "max_face_num": 5}
    params = urllib.parse.urlencode(params).encode(encoding='utf-8')
    request_url = request_url + "?access_token=" + access_token
    # 调用post请求方法
    face_info = get_info_post_json_data(request_url, params)
    # json字符串转对象
    face_json = json.loads(face_info)
    # print('face json is:')
    # print(face_json)
    # 如果没有发现人像，会返回空
    if face_json['result'] is None or face_json["result"]['face_num'] == 0:
        face_dict = {}
    else:
        # 把想要的部分提取存入字典中
        face_dict = face_json['result']['face_list']
    os.remove(img_path)
    return face_dict
