from app.models import Teacher,Lesson,LessonComment,LessonLabel
from collections import Counter
def getTeacherInfo(teacherID):
    thisTeacher = Teacher.objects.get(pk=teacherID)
    lessonObjList = Lesson.objects.filter(teacherObj=thisTeacher)
    lessonDic = {}
    lessonDicList = []
    sumJudge = 0.0
    x = 0
    for lesson in lessonObjList:
        lessonDic['courseName'] = lesson.lessonName
        lessonDic['courseJudge'] = lesson.lessonAverageJudge
        sumJudge += lesson.lessonAverageJudge
        lessonDic['averageScore'] = lesson.lessonAverage
        lessonDic['passRat'] = lesson.lessonPassRate
        lessonDic['people'] = lesson.lessonPeople
        lessonDic['index'] = x
        lessonDic['lessonID'] = lesson.pk
        x = x+1
        lessonDicList.append(lessonDic.copy())
    teacherJudge = sumJudge / len(lessonObjList)
    allDic = {}
    allDic['teacherName'] = thisTeacher.name
    allDic['school'] = thisTeacher.school
    allDic['teacherJudge'] = teacherJudge
    # 因为judge是肯定要读的,所以顺便算了并且保存
    thisTeacher.judge = teacherJudge
    putDisplayLabel(teacherID=teacherID)
    tempString = thisTeacher.teacherDisplayLabel
    labelList = tempString.split(',')
    allDic['tagList'] = labelList
    allDic['lessonDicList'] = lessonDicList
    thisTeacher.save()
    return allDic

def putDisplayLabel(teacherID):
    thisTeacher = Teacher.objects.get(pk=teacherID)
    commentObjList = LessonComment.objects.filter(lessonObj__teacherObj=thisTeacher)
    labelList = []
    for comment in commentObjList:
        labelObjList = LessonLabel.objects.filter(lessoncomment=comment)
        for labelObj in labelObjList:
            labelList.append(labelObj.label)
    count = Counter(labelList)
    topLabelDic = count.most_common(3)
    topLabelList = []
    for item,index in topLabelDic:
        tempString = item+ '('+str(index)+')'
        topLabelList.append(tempString)
    lastString = ','.join(topLabelList)
    thisTeacher.teacherDisplayLabel = lastString
    thisTeacher.save()
    return lastString
