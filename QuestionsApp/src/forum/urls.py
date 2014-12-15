from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_login, name='logout'),
    url(r'^createQuestion/$', views.create_question, name='createquestion'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/voteup/$', views.voteUp, name='voteup'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/votedown/$', views.voteDown, name='votedown'),
    url(r'^(?P<question_id>\d+)/votequp/$', views.voteQuestionUp, name='votequestionup'),
    url(r'^(?P<question_id>\d+)/voteqdown/$', views.voteQuestionDown, name='votequestiondown'),
    url(r'^(?P<question_id>\d+)/editquestion/$', views.edit_question, name='editquestion'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/editanswer/$', views.edit_answer, name='editanswer'),
)