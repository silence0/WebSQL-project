from django.conf.urls import url
from django.contrib import admin
import app.views
urlpatterns=[
    # url('^test$',app.views.test),
    url('^home$',app.views.home),
    url('^course/(?P<ID>[0-9]*)/$',app.views.course,name='course'),
    url('^offline$',app.views.offline),
    url('^logincheck$',app.views.log.logSubmit),
    url('^teacher/(?P<ID>[0-9]*)/$',app.views.teacher,name='teacher'),
    url('^ajaxto/$',app.views.ajaxTest2,name='to'),
    # url('^ajax/$',app.views.ajaxTest),
    url('^course/(?P<lessonID>[0-9]*)/comment/',app.views.getComment,name='commentPost'),
    url('^logout/$',app.views.logout),
    url('^search/(.*)$',app.views.search,name='search')
]