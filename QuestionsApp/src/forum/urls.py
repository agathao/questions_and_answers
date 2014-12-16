from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_login, name='logout'),
    url(r'^createQuestion/$', views.create_question, name='createquestion'),
    url(r'^upload_image/$', views.upload_image_view, name='upload_image'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/voteup/$', views.voteUp, name='voteup'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/votedown/$', views.voteDown, name='votedown'),
    url(r'^(?P<question_id>\d+)/votequp/$', views.voteQuestionUp, name='votequestionup'),
    url(r'^(?P<question_id>\d+)/voteqdown/$', views.voteQuestionDown, name='votequestiondown'),
    url(r'^(?P<question_id>\d+)/editquestion/$', views.edit_question, name='editquestion'),
    url(r'^(?P<question_id>\d+)/(?P<answer_id>\d+)/editanswer/$', views.edit_answer, name='editanswer'),
    url(r'^(?P<pk>\d+)/tag/$', views.FilteredIndexView.as_view(), name='filter_tag'),
    url(r'^(?P<pk>\d+)/rss/$', views.RSSView.as_view(), name='rss'),
) 