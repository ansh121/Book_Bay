from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from bookrequests import views

urlpatterns = patterns('',
	url(r'^lent/$', views.lent_index, name='lent'),
	url(r'^borrowed/$', views.borrowed_index, name='borrowed'),
	url(r'^accept/(?P<id>\d+)/$', views.accept, name='accept'),
	url(r'^reject/(?P<id>\d+)/$', views.reject, name='reject'),
	url(r'^return/(?P<id>\d+)/$', views.return_book, name='return'),
)

urlpatterns += staticfiles_urlpatterns()