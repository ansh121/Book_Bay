from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from bookzilla import views

urlpatterns = patterns('',
	# index page
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^admin/', include(admin.site.urls)),
    
    # the users module
    url(r'^users/', include('users.urls', namespace='users')),
    # courier module
    url(r'^courier/', include('courier.urls', namespace='courier')),
)

urlpatterns += staticfiles_urlpatterns()


