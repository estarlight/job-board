from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register, name='register'),
    url(r'login$', views.login, name='login'),
    url(r'^logout', views.logout),
    url(r'^dashboard', views.dashboard),
    url(r'^createjob$', views.createjob),
    url(r'^create_process', views.create_process),
    url(r'^addjob/(?P<id>\d+)', views.addjob),
    url(r'^edit/(?P<id>\d+)', views.edit),
    url(r'^edit_process', views.edit_process),
    url(r'^view/(?P<id>\d+)', views.view),
    url(r'^cancel/(?P<id>\d+)', views.cancel),
    url(r'^done/(?P<id>\d+)', views.cancel),

]