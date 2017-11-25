
from django.db import models

# Create your models here.

class Student(models.Model):
    name=models.CharField('姓名',max_length=20)
    studentID=models.CharField("用户名",max_length=20)
    lessonObj=models.ManyToManyField("Lesson", through="LessonComment")
    # studentPSW = models.CharField("密码",max_length=20,blank=True)

class LessonComment(models.Model):
    studentObj=models.ForeignKey(Student)
    lessonObj=models.ForeignKey("Lesson")
    lessonLabelObj = models.ManyToManyField("LessonLabel")
    semester=models.BooleanField("本学期课程",default=False)
    commented=models.BooleanField("是否已经评价",default=False)
    grade = models.IntegerField("该门课的成绩",default=0)
    lessonJudge = models.IntegerField("该学生对这门课的评价分数",default=5)
    lessonDetailJudge = models.TextField("该学生对这门课的自由评价",default="")
    commentDate = models.DateField("评价时间",auto_now_add=True)


class Lesson(models.Model):
    lessonNumA = models.CharField("课程号",max_length=20)
    lessonNumB = models.CharField("课程序号",max_length=4)
    lessonName = models.CharField("课程名",max_length=100)
    teacherObj = models.ForeignKey("Teacher", on_delete=models.CASCADE, verbose_name="授课教师")
    lessonCredit = models.IntegerField("学分",default=2)
    lessonAverage = models.FloatField("平均分",default=0)
    lessonPassRate = models.FloatField("通过率",default=0)
    lessonPeople = models.IntegerField("拥有该课程成绩的人数",default=0)
    lessonAverageJudge = models.FloatField("课程的综合评价分数",default=5)
    lessonDisplayLabel = models.TextField("要展示的这门课程的标签,逗号作为分割",default="")
    commentNum = models.IntegerField("评价人数",default=0)


#老师页面的评价就先用课程的吧
class Teacher(models.Model):
    name = models.CharField("姓名",max_length=100)
    school = models.CharField("学院",max_length=40)
    judge = models.FloatField("评分",default=5)
    teacherDisplayLabel = models.TextField("要展示的这个老师的标签,逗号作为分割", default="")


#这个东西目前没有用
class Comment(models.Model):
    teacherObj = models.ManyToManyField(Teacher)
    comment = models.CharField(verbose_name="评价标签",max_length=20)


class LessonLabel(models.Model):
    label = models.CharField("标签名称",max_length=20,unique=True,default="")

