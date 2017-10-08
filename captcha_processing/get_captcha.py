from PIL import Image
from seleniumrequests import PhantomJS
import requests
myDriver=PhantomJS(r"D:\phantomjs-2.1.1-windows\bin\phantomjs")
captchaUrl=r"http://jwk.lzu.edu.cn/academic/getCaptcha.do?0.6723898265425539"
for i in range(1,201):
    temp=requests.get(captchaUrl)
    myImage=open("%d.jpg"%(i),'wb')
    myImage.write(temp.content)
    myImage.close()

for i in range(1,201):
    myImage2=Image.open("%d.jpg"%(i))
    assert isinstance(myImage2,Image.Image)
    myImage2=myImage2.convert('L')
    myImage2.save("h%d.jpg"%(i))

matrix=[]
x=60
for i in range(256):
    if i <x:
        matrix.append(0)
    else:
        matrix.append(1)
for i in range(1,201):
    myImage3=Image.open("h%d.jpg"%(i))
    assert isinstance(myImage3,Image.Image)
    myImage3.point(matrix,'1').save("er%d.tif"%(i))