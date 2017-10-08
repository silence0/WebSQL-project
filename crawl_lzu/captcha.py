#TODO:因为我的账户没有进行成绩审查,所以目前不能对数据测试,但是四六级成绩是可以查看的,并且成功了.
from PIL import Image
import time
from bs4 import BeautifulSoup
from seleniumrequests import PhantomJS
myDriver =PhantomJS(r"D:\phantomjs-2.1.1-windows\bin\phantomjs")
captchaUrl="http://jwk.lzu.edu.cn/academic/getCaptcha.do;jsessionid=3544AED4E1F967CA2B0AAF4CAC0E46F5.TA3?0.9214071135670294"
checkUrl="http://jwk.lzu.edu.cn/academic/j_acegi_security_check"
wantUrl="http://jwk.lzu.edu.cn/academic/index_new.jsp"
myPost={}
# myDriver.get(checkUrl)
# myDriver.save_screenshot("./cap.png")
# captcha=Image.open("./cap.png")
# Image._show(captcha)
# inputCaptcha=input("please input the captcha:")
# myPost["j_captcha"]=inputCaptcha
# print(myPost)
# temp=myDriver.request("post",checkUrl)
# time.sleep(5)

# myDriver.get(wantUrl)
#
#
# myDriver.get_screenshot_as_file("./screenshot.png")
#
# Image._show(Image.open("./screenshot.png"))
username=input("please input your username:")
password=input("please input your passwrod:")
myPost["j_password"]=password
myPost["j_username"]=username
myDriver.get(checkUrl)
myDriver.get_screenshot_as_file("temp.jpg")
im=Image.open("temp.jpg")
Image._show(im)
myDriver.find_element_by_name("j_username").send_keys(username)
myDriver.find_element_by_name("j_password").send_keys(password)
captcha=input("please input the captcha:")
myDriver.find_element_by_name("j_captcha").send_keys(captcha)
myDriver.find_element_by_name("button1").click()
myDriver.get_screenshot_as_file("temp2.jpg")
im2=Image.open("temp2.jpg")
Image._show(im2)
print(myDriver.get_cookies())
gradeUrl='http://jwk.lzu.edu.cn/academic/accessModule.do?moduleId=2090&groupId='
myDriver.get(gradeUrl)
myDriver.get_screenshot_as_file("temp3.jpg")
