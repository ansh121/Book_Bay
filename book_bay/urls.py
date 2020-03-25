"""book_bay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bookbayapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.userdetails, name='register'),
    path('login/', views.validatelogin, name='login'),
    path('userhome/', views.userhome, name='userhome'),
    path('searchresult/', views.searchresult, name='searchresult'),
    path('mybooks/', views.mybooks, name='mybooks'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('', views.home, name='home'),
    #path('userdetails/', views.userdetails),
]

urlpatterns += staticfiles_urlpatterns()