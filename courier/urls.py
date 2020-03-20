from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from courier import views

urlpatterns = patterns('',
	url(r'^login/$', views.login, name='login'),
	url(r'^home/$', views.home, name='home'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^advance/(?P<req_id>\d+)/$', views.advance_request, name='advance'),
)

urlpatterns += staticfiles_urlpatterns()