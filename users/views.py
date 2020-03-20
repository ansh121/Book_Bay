from django.shortcuts import render

from django.core.urlresolvers import reverse

from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.models import UserInfo

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from bookzilla.misc import anonymous_required

@login_required
def logout(request):
    djlogout(request)
    return render(request, 'logout.html')

@anonymous_required
def login(request):
    # check if the form was submitted
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # next page to redirect to
        next_url = request.POST.get('next')

        # default redirect
        if not next_url:
            next_url = reverse('users:home')

        user = authenticate(username=username, password=password)

        if user is not None:
            djlogin(request, user)

            return HttpResponseRedirect(next_url)
        else:
            messages.error(request,
             'The username or password you entered is incorrect')

            return render(request, 'login.html')
    else:
        # go to the login page
        return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

@anonymous_required
def register(request):
    

    if request.method == 'POST':
        message = ''

        username = request.POST.get('username')
        email    = request.POST.get('email')  
        fname    = request.POST.get('firstName')  
        lname    = request.POST.get('lastName')  
        address  = request.POST.get('address')  
        dob      = request.POST.get('dob')  
        password = request.POST.get('password')  

        inputs = (username, email, 
                fname, lname, address,
                address, dob, password)   

        if User.objects.filter(username__exact=username).exists():
            message = 'name_taken'

        elif User.objects.filter(email__exact=email).exists():
            message = 'email_taken'
        
        if not message:
            # create a new user 
            try:
                new_user = User.objects.create_user(
                                username=username, email=email, password=password,
                                first_name=fname,
                                last_name=lname
                            )

                new_user_info = UserInfo(user = new_user, address = address, dob = dob)
                new_user_info.save()
                djlogin(request, new_user)

            except Exception, e:
                print str(e)
            
            message = "no_error"

        return HttpResponse(message) 
    else:
        return render(request, 'register.html')