import django

django.setup()
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from app import saveStudentInfo
from django.http import JsonResponse
from django.shortcuts import redirect
from app.homeinfo import getInfoObj, getInfoObjByLessonList,getTopLessonObjList
from app.homeinfo import caculateForGrade
from app.courseinfo import getCourseInfo
from app.courseinfo import putComment
from app.teacherinfo import getTeacherInfo
from app.serach import searchByLesson, searchByTeacher, notFoundException



# Create your views here.
class log:
    # def logGetCaptcha(request):
    #     link = sessions.session()
    #     captchaurl='http://jwk.lzu.edu.cn/academic/getCaptcha.do?'
    #     pic = link.get(captchaurl)
    #     a = base64.encodebytes(pic.content)
    #     assert isinstance(request,WSGIRequest)
    #     request.session['JSESSIONID']=link.cookies.get(name='JSESSIONID')
    #     return render(request,template_name=r'app/log.html',context={'captcha':a})
    def logSubmit(request):
        assert isinstance(request, WSGIRequest)
        id = request.POST['userID']
        pw = request.POST['userPassword']
        if id == '1' and pw == '1':
            id = '320150938821'
            pw = 'BaI19970909'
        # userName JSESSIONID是在toplog里面存放的
        get = saveStudentInfo.toplog(request, id, pw)
        if isinstance(get, dict):
            return HttpResponse({'error': 'error'})
            # 说明用户名或者密码之类的错了
        else:
            # 成功了之后,让你进入一个地方
            # 直接就把这个学生所有数据导入了,然后保持连接
            # 因为某些历史原因,session.id 就在外面赋值了
            request.session['userID'] = id
            request.session['log'] = True
            # return render(request,r'app/index.html')
            return redirect('/app/home')


def home(request):
    caculateForGrade()
    try:
        userID = request.session['userID']
    except:
        return redirect(r'/app/offline')
    infoObjList = getInfoObj(request.session['userID'])
    userName = request.session['userName']
    topLessonObjList = getTopLessonObjList()
    outTopList = []
    for i in topLessonObjList:
        thisObjStr = {}
        thisObjStr['topName'] = i.lessonName
        thisObjStr['topID'] = i.pk
        thisObjStr['topIndex'] = topLessonObjList.index(i)+1
        outTopList.append(thisObjStr.copy())
    alldict = {
        'infoObjList': infoObjList,
        'userName': userName,
        'topList':outTopList
    }
    return render(request, r'app/index.html', context=alldict)


def course(request, ID):
    assert isinstance(request, HttpRequest)
    dic = getCourseInfo(ID)
    try:
        dic['userName'] = request.session['userName']
    except:
        return redirect(r'/app/offline')
    infoObjList = getInfoObj(request.session['userID'])
    userName = request.session['userName']
    topLessonObjList = getTopLessonObjList()
    outTopList = []
    for i in topLessonObjList:
        thisObjStr = {}
        thisObjStr['topName'] = i.lessonName
        thisObjStr['topID'] = i.pk
        thisObjStr['topIndex'] = topLessonObjList.index(i)+1
        outTopList.append(thisObjStr.copy())

    dic['topList'] = outTopList
    return render(request, r'app/course.html', context=dic)


def offline(request):
    return render(request, r'app/offline.html')


def teacher(request, ID):
    allDic = getTeacherInfo(ID)
    try:
        allDic['userName'] = request.session['userName']
    except:
        return redirect(r'/app/offline')

    topLessonObjList = getTopLessonObjList()
    outTopList = []
    for i in topLessonObjList:
        thisObjStr = {}
        thisObjStr['topName'] = i.lessonName
        thisObjStr['topID'] = i.pk
        thisObjStr['topIndex'] = topLessonObjList.index(i)+1
        outTopList.append(thisObjStr.copy())
    allDic['topList'] = outTopList
    return render(request, r'app/teacher.html', context=allDic)


def ajaxTest2(request):
    mylist = [1, 2, 3, 4, 5]
    return JsonResponse(mylist, safe=False)


def getComment(request, lessonID):
    judge = request.POST['star']
    text = request.POST['commentText']
    tagString = request.POST['tag']
    try:
        userID = request.session['userID']
    except:
        return redirect(r'/app/offline')
    putComment(request.session['userID'], lessonID=lessonID, judge=judge, tagString=tagString, text=text)
    return redirect(r'/app/course/' + lessonID)


def logout(request):
    request.session.clear()
    return redirect(r'/app/offline')


def search(request, searchStr):
    lessonObjSet = set()
    temp1 = searchByLesson(searchStr)
    temp2 = searchByTeacher(searchStr)
    for i in temp1:
        lessonObjSet.add(i)
    for i in temp2:
        lessonObjSet.add(i)
    infoObjList = getInfoObjByLessonList(lessonObjSet)
    userName = request.session['userName']
    topLessonObjList = getTopLessonObjList()
    outTopList = []
    for i in topLessonObjList:
        thisObjStr = {}
        thisObjStr['topName'] = i.lessonName
        thisObjStr['topID'] = i.pk
        thisObjStr['topIndex'] = topLessonObjList.index(i) +1
        outTopList.append(thisObjStr.copy())
    alldic = {
        'infoObjList': infoObjList,
        'userName': userName,
        'topList' :outTopList,
    }
    return render(request,r'app/index.html', context=alldic)
