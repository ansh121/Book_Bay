from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from users import views

#import notifications

urlpatterns = patterns('',
	url(r'^home/$', views.home, name='home'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),		

	# books module
	url(r'^books/', include('books.urls', namespace='books')),
	# bookrequests module
	url(r'^requests/', include('bookrequests.urls', namespace='requests')),
	# notifications
    #url('^inbox/notifications/', include(notifications.urls)),
)

urlpatterns += staticfiles_urlpatterns()