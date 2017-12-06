from django import setup

setup()
from app.models import Lesson, LessonLabel, LessonComment, Student
from collections import Counter
import datetime
from django.db import models
from app.teacherinfo import putDisplayLabel

def getCourseInfo(ID):
    # 为了前端获取课程的各种信息
    thisLesson = Lesson.objects.get(pk=ID)
    lessonName = thisLesson.lessonName
    teacherName = thisLesson.teacherObj.name
    schoolName = thisLesson.teacherObj.school
    sumJudge = thisLesson.lessonAverageJudge
    lessonCommentTextList = []
    # 这个是打分
    lessonJudge = []
    lessonCommentDate = []
    lessonCommentList = LessonComment.objects.filter(lessonObj=thisLesson, commented=True)
    for lessonCommentObj in lessonCommentList:
        lessonCommentTextList.append(lessonCommentObj.lessonDetailJudge)
        lessonJudge.append(lessonCommentObj.lessonJudge)
        lessonCommentDate.append(lessonCommentObj.commentDate)
    # 这个people是lesson里面的属性,是指有这门课成绩的人
    people = thisLesson.lessonPeople
    passRat = thisLesson.lessonPassRate
    average = thisLesson.lessonAverage
    lessonPartLabelList = str.split(thisLesson.lessonDisplayLabel, ',')
    peopleCommentObjList = []
    commentNum = len(lessonCommentList)
    for i in range(0, len(lessonCommentList)):
        peopleCommentObj = {}
        peopleCommentObj['judge'] = lessonJudge[i]
        peopleCommentObj['text'] = lessonCommentTextList[i]
        peopleCommentObj['date'] = lessonCommentDate[i]
        peopleCommentObj['index'] = i
        peopleCommentObjList.append(peopleCommentObj.copy())

    dic = {
        'course': lessonName,
        'teacher': teacherName,
        'people': people,
        'judge': sumJudge,
        'passRat': passRat,

        # 这个是大家对这门课程的总体评价
        'tag': lessonPartLabelList,
        'average': float("%.2f"%average),
        'schoolName': schoolName,
        'peopleObj': peopleCommentObjList,
        'commentNum': commentNum
    }
    return dic


def putTopLabel(lessonID):
    # 在数据库中保存这门课程大家对他的评价标签(前三位),然后返回这个list
    num = 3
    thisLesson = Lesson.objects.get(pk=lessonID)
    # 获取这门课所有的评价
    commentList = LessonComment.objects.filter(lessonObj=thisLesson)
    labelList = []
    for obj in commentList:
        # 获取这门课程,这个评价条的所有标签
        subLabelObjList = LessonLabel.objects.filter(lessoncomment=obj)
        for labelObj in subLabelObjList:
            labelList.append(labelObj.label)
    counterLabelList = Counter(labelList)
    out = counterLabelList.most_common(num)
    tempArray = []
    for item, index in out:
        outString = ''
        outString = outString + item + '(' + str(index) + ')'
        tempArray.append(outString)
    outString = ','.join(tempArray)
    thisLesson.lessonDisplayLabel = outString
    thisLesson.save()
    return outString


def putAverageJudge(lessonID):
    # 在数据库里面存放这门课程的平均评价分数
    lessonObj = Lesson.objects.get(pk=lessonID)
    commentList = LessonComment.objects.filter(lessonObj=lessonObj)
    sum = 0.0
    for comment in commentList:
        sum += comment.lessonJudge
    lessonObj.lessonAverageJudge = sum / len(commentList)
    lessonObj.save()


def putStudentTag(studentID, lessonID, tagString):
    # 把同学对于课程的评价放到数据库里面
    studentObj = Student.objects.get(studentID=studentID)
    lessonObj = Lesson.objects.get(pk=lessonID)
    commentObj = LessonComment.objects.get(studentObj=studentObj, lessonObj=lessonObj)
    assert isinstance(tagString, str)
    tagList = tagString.split(',')
    commentObj.lessonLabelObj.clear()
    for tag in tagList:
        try:
            tagObj = LessonLabel.objects.get(label=tag)
        except:
            tagObj = LessonLabel(label=tag)
            tagObj.save()
        commentObj.lessonLabelObj.add(tagObj)
    commentObj.save()


def putStudentJudge(studentID, lessonID, judge):
    studentObj = Student.objects.get(studentID=studentID)
    lessonObj = Lesson.objects.get(pk=lessonID)
    commentObj = LessonComment.objects.get(studentObj=studentObj, lessonObj=lessonObj)
    commentObj.lessonJudge = judge
    commentObj.save()


def putStudentDetailComment(studentID, lessonID, text):
    studentObj = Student.objects.get(studentID=studentID)
    lessonObj = Lesson.objects.get(pk=lessonID)
    commentObj = LessonComment.objects.get(studentObj=studentObj, lessonObj=lessonObj)
    commentObj.lessonDetailJudge = text
    commentObj.commented = True
    commentObj.commentDate = datetime.date.today()
    commentObj.save()


def putComment(studentID, lessonID, judge, tagString, text):
    putStudentJudge(studentID=studentID, lessonID=lessonID, judge=judge)
    putStudentTag(studentID, lessonID, tagString)
    putStudentDetailComment(studentID, lessonID, text)
    putTopLabel(lessonID=lessonID)
    putAverageJudge(lessonID)
