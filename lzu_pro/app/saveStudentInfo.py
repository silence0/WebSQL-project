import django

django.setup()
import requests
from bs4 import BeautifulSoup
from app.models import Student, Teacher, Lesson, LessonComment
from app.getjess import getJess


def getname(uid):
    # 由教务在线的token获取这个人的姓名,是一个内部的方法
    infourl = r'http://jwk.lzu.edu.cn/academic/student/studentinfo/studentInfoModifyIndex.do?frombase=0&wantTag=0&groupId=&moduleId=2060'
    link = requests.session()
    link.cookies.set('JSESSIONID', uid)
    a = link.get(infourl)
    bf = BeautifulSoup(a.content)
    out = bf.find_all(name='tr')
    x = out[1]
    temp = x.find(name='td')
    return (temp.text.strip())


def savelesson(studentId, uid, year, term):
    #这也是一个内部方法,用来在课程页查询这个学生的课程信息,并且保存在数据库里面
    studentName = getname(uid=uid)
    try:
        tempstudentobj = Student.objects.get(studentID=studentId)
    except:
        # 放学生用户
        tempstudentobj = Student(studentID=studentId, name=studentName)
        tempstudentobj.save()

    link = requests.session()
    link.cookies.set('JSESSIONID', uid)
    oriurl = r'http://jwk.lzu.edu.cn/academic/student/currcourse/currcourse.jsdo?'
    url = oriurl + 'year=' + year + '&' + 'term=' + term
    lessonHTML = link.get(url)
    temp = lessonHTML.text
    bs = BeautifulSoup(temp)
    temp = bs.find(name='table', class_='infolist_tab')
    temp2 = temp.find_all(name='tr', class_='infolist_common')
    allresult = temp2
    out = {}
    number1 = []
    number2 = []
    lesson = []
    teacher = []
    for i in allresult:
        number1.append(i.find_all(name='td')[0].text.strip())
        number2.append(i.find_all(name='td')[1].text.strip())
        lesson.append(i.find_all(name='td')[2].text.strip())
        teacher.append(i.find_all(name='td')[3].text.strip())

    # for i in range(0, len(allresult), 2):
    #     if i + 1 >= len(allresult):
    #         break
    #     out[allresult[i].string.strip()] = allresult[(i + 1)].string.strip()
    # for i, j in out.items():
    #     lesson.append(i)
    #     teacher.append(j)
    #
    # temp = bs.find_all(name="tr", class_="infolist_common")
    # for i in range(0, len(teacher)):
    #     number1.append(temp[i].find_next(name="td").string.strip())
    #     number2.append(temp[i].find_next(name="td").find_next(name="td").string.strip())
    tempteacherid = []
    # 先放老师
    for te in teacher:
        try:
            temp = Teacher.objects.get(name=te)
        except:
            temp = Teacher(name=te)
            temp.save()
        tempteacherid.append(temp.id)
    # 放课程
    templessonobj = []
    for i in range(0, len(lesson)):
        try:
            temp = Lesson.objects.get(lessonNumA=number1[i], lessonNumB=number2[i])
        except:
            temp = Lesson(lessonName=lesson[i], lessonNumA=number1[i], lessonNumB=number2[i],
                          teacherObj=Teacher.objects.get(pk=tempteacherid[i]), lessonCredit=2)
            temp.save()
        templessonobj.append(temp)

    # 中间表把学生和课程联系起来
    for i in templessonobj:
        try:
            LessonComment.objects.get(studentObj=tempstudentobj, lessonObj=i)
        except:
            temp = LessonComment(studentObj=tempstudentobj, lessonObj=i)
            temp.save()


posturl = r'http://jwk.lzu.edu.cn/academic/j_acegi_security_check'
captchaurl = 'http://jwk.lzu.edu.cn/academic/getCaptcha.do?'
geturl = r'http://jwk.lzu.edu.cn/academic/student/studentinfo/studentInfoModifyIndex.do?frombase=0&wantTag=0&groupId=&moduleId=2060'
gradeposturl = r'http://jwk.lzu.edu.cn/academic/manager/score/studentOwnScore.do?groupId=&moduleId=2021'
gradegeturl = r'http://jwk.lzu.edu.cn/academic/calendar/showCalendarYearTerm.do?type=alias&yearId=37&termId='


def savegrade(studentId, uid, year):
    #这个其实和上一个保存课程的东西差不多,只不过分开来做,这个是保存它的成绩信息
    gradedic = {
        'year': '36',
        'term': '',
        'para': '0',
        'sortColumn': '',
        'Submit': '查询'
    }
    gradedic['year'] = year
    link = requests.session()
    link.cookies.set('JSESSIONID', uid)
    temp = link.post(gradeposturl, gradedic)
    bf = BeautifulSoup(temp.text)
    t_all = bf.find_all(name='td')
    t_all.pop(0)
    t_all.pop(0)
    t_all.pop(0)
    t_all.pop(0)
    lessonNumA = []
    lessonNumB = []
    lessonName = []
    lessonGrade = []
    for k in range(0, (len(t_all) // 18)):
        plus = k * 18
        lessonNumA.append(t_all[plus + 2].text.strip())
        lessonName.append(t_all[plus + 3].text.strip())
        lessonNumB.append(t_all[plus + 4].text.strip())
        lessonGrade.append(t_all[plus + 8].text.strip())
    for a, b, c, d in zip(lessonNumA, lessonNumB, lessonName, lessonGrade):
        try:
            templesson = Lesson.objects.get(lessonNumA=a, lessonNumB=b)
            t = LessonComment.objects.get(studentObj=Student.objects.get(studentID=studentId), lessonObj=templesson)
            t.grade = d
            t.save()
        except:
            pass


def toplog(request, username, password):
    #这个是可以外部使用的方法,用来导入学生一切的信息
    jess = getJess(username, password=password)
    # 如果返回的是一个包含错误的字典
    if isinstance(jess, dict):
        return jess
    request.session['JSESSIONID'] = jess
    request.session['userName'] = getname(jess)

    for i in range(35, 38):
        savelesson(username, jess, i.__str__(), '1')
        savelesson(username, jess, i.__str__(), '2')

    savegrade(username, jess, '36')
    savegrade(username, jess, '37')
    savegrade(username, jess, '35')
    return True

# toplog(username='320150929031',password='yxl520256')
# toplog(username='320150938821',password='BaI19970909')
