from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login_handler, name='login_handler'),
    url(r'^logout/$', views.logout_handler, name='logout_handler'),
    url(r'^sessions/$', views.sessions, name='sessions'),
    url(r'^sessions/(?P<pk>[0-9]+)/$', views.sessions, name='sessions'),
]
