from django.test import TestCase
from django.http import JsonResponse
from bs4 import BeautifulSoup
# Create your tests here.
from aip import AipOcr
import requests
from bs4 import BeautifulSoup
from urllib import parse
import json
import base64

def getJess(username,password):
    captchaurl = 'http://jwk.lzu.edu.cn/academic/getCaptcha.do?'
    posturl = r'http://jwk.lzu.edu.cn/academic/j_acegi_security_check'
    APP_ID = '10281345'
    API_KEY = 'Rdb7GHl0x8BVoczAfqYGyBY6'
    SECRET_KEY = 'EpYQqlQqCf54FcBmIWBSZkhaEvWvf8VY'
    link = requests.session()
    while True:
        aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        pic = link.get(captchaurl)
        result = aipOcr.basicGeneral(pic.content)
        result = result['words_result'][0]['words']
        dic = {

            'j_username': username,
            'j_password': password,
            'j_captcha': result,
            'groupId': '',
        }
        html = link.post(posturl,data=dic)
        error = logError(html)
        if error['code']=='0':
            return link.cookies.get('JSESSIONID')
        elif error['code']=='1':
            continue
        else:
            return error


def logError (html):
    bs=BeautifulSoup(html.text)
    try:
        t = bs.find(name='div',id='error')
        info = t.text.strip()
        if "验证码" in info:
            return ({'code':'1','error':'验证码错误','goon':True} )
        if "密码"   in info:
            return ({'code':'2','error':'密码错误','goon':False})
        if "用户名" in info:
            return ({'code':'3','error':'用户名不存在','goon':False})
    except:
        return ({'code':'0','eroor':'不存在错误','goon':False})
