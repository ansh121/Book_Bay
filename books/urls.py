from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from books import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^add_book/$', views.add_book, name='add_book'),
	url(r'^edit_book/(?P<book_id>\d+)/$', views.edit_book, name='edit_book'),
	url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
	url(r'^search/$', views.search, name='search'),
	url(r'^make_request/(?P<id>\d+)/$', views.make_request, name='make_request'),
)

urlpatterns += staticfiles_urlpatterns()