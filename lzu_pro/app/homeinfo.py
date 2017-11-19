from django import setup
setup()
from app.models import *
from django.db.models.fields import related_descriptors
def getInfoObj(userID):
    # userID='320150939151'
    thisStudent = Student.objects.get(studentID=userID)
    lessonObjList = Lesson.objects.filter(lessoncomment__studentObj=thisStudent)
    teacherObjList=[]
    schoolNameList = []
    peopleList = []
    averageList = []
    passRateList = []
    teacherIDList=[]
    courseIDList=[]
    judgeList = []
    #这里的teacherID其实是teacherobject,因为历史原因写错了..lessonID也是这样
    for lessonObj in lessonObjList:
        tempTeacher = lessonObj.teacherObj
        teacherIDList.append(tempTeacher.pk)
        teacherObjList.append(tempTeacher)
        schoolNameList.append(tempTeacher.school)
        peopleList.append(lessonObj.lessonPeople)
        averageList.append(lessonObj.lessonAverage)
        passRateList.append(lessonObj.lessonPassRate)
        judgeList.append(lessonObj.lessonAverageJudge)
    lessonNameList = []
    teacherNameList = []
    for i in lessonObjList:
        lessonNameList.append(i.lessonName)
        courseIDList.append(i.pk)
    for i in teacherObjList:
        teacherNameList.append(i.name)
    infoobjlist=[]


    # topLessonObjList = getTopLessonObjList()
    # outTopList = []
    # for i in topLessonObjList:
    #     thisObjStr = {}
    #     thisObjStr['topName'] = i.lessonName
    #     thisObjStr['topID'] = i.pk
    #     thisObjStr['topIndex'] = topLessonObjList.index(i)
    #     outTopList.append(thisObjStr.copy())

    for i in range(0,len(lessonNameList)):
        infoobj = {
            'course': lessonNameList[i],
            'school': schoolNameList[i],
            'grade': averageList[i],
            'teacher': teacherNameList[i],
            'pass': passRateList[i],
            'people': peopleList[i],
            'courseID':courseIDList[i],
            'teacherID':teacherIDList[i],
            'judge':judgeList[i],
            'index':i,
            # 'topList':outTopList
        }
        infoobjlist.append(infoobj.copy())
    return infoobjlist
def caculateForGrade():
    '''计算平均分什么的,跟评价无关'''
    lessonObjList = Lesson.objects.filter()
    for lessonObj in lessonObjList:
        sumGrade = 0
        passPeople = 0
        tempGradeObjList = LessonComment.objects.filter(lessonObj=lessonObj)
        people = LessonComment.objects.filter(lessonObj=lessonObj).count()
        for gradeObj in tempGradeObjList:
            sumGrade = sumGrade + gradeObj.grade
            if gradeObj.grade >= 60:
                passPeople = passPeople + 1
            #等于0认为是没有成绩,所以总人数要减去1
            if gradeObj.grade == 0:
                people = people - 1
        if people == 0:
            lessonObj.lessonAverage = 0
            lessonObj.lessonPassRate = 0
            lessonObj.lessonPeople = people
            lessonObj.save()
        else:
            lessonObj.lessonAverage = sumGrade / people
            lessonObj.lessonPassRate = passPeople / people
            lessonObj.lessonPeople = people
            lessonObj.save()

def getInfoObjByLessonList(inLessonObjList):
    # userID='320150939151'
    # thisStudent = Student.objects.get(studentID=userID)
    lessonObjList = inLessonObjList
    teacherObjList=[]
    schoolNameList = []
    peopleList = []
    averageList = []
    passRateList = []
    teacherIDList=[]
    courseIDList=[]
    judgeList = []
    #这里的teacherID其实是teacherobject,因为历史原因写错了..lessonID也是这样
    for lessonObj in lessonObjList:
        tempTeacher = lessonObj.teacherObj
        teacherIDList.append(tempTeacher.pk)
        teacherObjList.append(tempTeacher)
        schoolNameList.append(tempTeacher.school)
        peopleList.append(lessonObj.lessonPeople)
        averageList.append(lessonObj.lessonAverage)
        passRateList.append(lessonObj.lessonPassRate)
        judgeList.append(lessonObj.lessonAverageJudge)
    lessonNameList = []
    teacherNameList = []
    for i in lessonObjList:
        lessonNameList.append(i.lessonName)
        courseIDList.append(i.pk)
    for i in teacherObjList:
        teacherNameList.append(i.name)
    infoobjlist=[]
    for i in range(0,len(lessonNameList)):
        infoobj = {
            'course': lessonNameList[i],
            'school': schoolNameList[i],
            'grade': averageList[i],
            'teacher': teacherNameList[i],
            'pass': passRateList[i],
            'people': peopleList[i],
            'courseID':courseIDList[i],
            'teacherID':teacherIDList[i],
            'judge':judgeList[i],
            'index':i
        }
        infoobjlist.append(infoobj.copy())
    return infoobjlist

def getTopLessonObjList():
    allLessonObjList = Lesson.objects.filter()
    count = []
    for i in allLessonObjList:
        x = len(LessonComment.objects.filter(lessonObj=i))
        count.append(x)
    index = []
    for i in range(0,10):
        x = count.index(max(count))
        index.append(x)
        count[x] = -1
    topObjList = []
    for i in index:
        topObjList.append(allLessonObjList[i])
    return topObjList