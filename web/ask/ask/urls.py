from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from qa import views

urlpatterns = patterns('',
    url(r'^$', views.question_list, {'sort': 'newest'}),
    url(r'^login/$', views.test),
    url(r'^signup/$', views.test),
    url(r'^question/(?P<qid>[0-9]+)/$', views.question_details, name='question-details'),
    url(r'^ask/', views.askform),
    url(r'^answer/', views.post_answer),
    url(r'^popular/$', views.question_list, {'sort': 'popular'}),
    url(r'^new/$', views.test),
)
