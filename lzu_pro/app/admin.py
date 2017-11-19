from django.contrib import admin
from app.models import Student,Teacher,Lesson,LessonComment,Comment
# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(LessonComment)
admin.site.register(Lesson)
admin.site.register(Comment)