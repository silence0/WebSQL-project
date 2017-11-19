from app.models import *


class notFoundException(Exception):
    pass


def searchByTeacher(teacherName):
    teacherObjList = Teacher.objects.filter(name__contains=teacherName)
    if (len(teacherObjList) == 0):
        return []
    lessonObjList = []
    for i in teacherObjList:
        lessonObjOfThisTeacher = Lesson.objects.filter(teacherObj= i )
        for j in lessonObjOfThisTeacher:
            lessonObjList.append(j)
    return lessonObjList
def searchByLesson(lessonName):
    lessonObjList = Lesson.objects.filter(lessonName__contains=lessonName)
    if (len(lessonObjList) ==0):
        return []
    return lessonObjList