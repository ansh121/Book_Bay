from django.shortcuts import render, redirect
from bookbayapp.forms import *
from bookbayapp.models import *
from django.http import HttpResponse


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

        try:
            user = User.objects.create(user_id = userid ,email_address = email,name = name,house_number = house_no,street = street,locality = locality,postal_code = postal_code,landmark = landmark,city = city,state = state)
            new_credentials = LoginCredential(user=user, password=password)
            new_credentials.save()
        except:
            return HttpResponse('error')

        return HttpResponse("no error")

    else:
        return render(request, 'register.html')
