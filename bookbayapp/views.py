from django.shortcuts import render, redirect
from bookbayapp.forms import *
from bookbayapp.models import *
from django.http import HttpResponse


def home(request):
    return render(request,'home.html')


def validatelogin(request):
    if request.method=="POST":
        userid = request.POST.get("username")
        password = request.POST.get("password")
        message = ''

        if LoginCredential.objects.filter(user_id__exact=userid).exists():
            user_cred=LoginCredential.objects.get(user_id=userid)

            if user_cred.password == password:
                message = 'no_error'
            else:
                message ='password_mismatch'

        else:
            message = 'user_id_not_found'

        return HttpResponse(message)
    else:
        return render(request, 'login.html')


def userdetails(request):
    if request.method == "POST":
        userid = request.POST.get("username")
        email = request.POST.get("email")
        name = request.POST.get("name")
        house_no = request.POST.get("house_no")
        street = request.POST.get("street")
        locality = request.POST.get("locality")
        postal_code = request.POST.get("postal_code")
        landmark = request.POST.get("landmark")
        city = request.POST.get("city")
        state = request.POST.get("state")
        password = request.POST.get("password")

        message=""
        if User.objects.filter(user_id__exact=userid).exists():
            message = 'name_taken'

        elif User.objects.filter(email_address__exact=email).exists():
            message = 'email_taken'

        if not message:
            try:
                user = User.objects.create(user_id = userid ,email_address = email,name = name,house_number = house_no,street = street,locality = locality,postal_code = postal_code,landmark = landmark,city = city,state = state)
                new_credentials = LoginCredential(user=user, password=password)
                new_credentials.save()

            except:
                return print('error')

            message = "no_error"
        return HttpResponse(message)

    else:
        return render(request, 'register.html')
