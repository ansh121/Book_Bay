from django.shortcuts import render, redirect
from bookbayapp.forms import *
from bookbayapp.models import *
from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as djUser

from django.contrib import messages
from django.db import connection, transaction


def perform_raw_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    list = []
    i = 0
    for row in results:
        dict = {}
        field = 0
        while True:
            try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field +1
            except IndexError as e:
                break
        i = i + 1
        list.append(dict)
    return list

@login_required()
def searchresult(request):
    user = request.user
    if request.method=="POST":
        search = request.POST.get('search')
        print(search)
        namebooks = Book.objects.filter(book_name__contains=search)
        isbnbooks = Book.objects.filter(isbn__exact=search)
        books = namebooks | isbnbooks
        books = books.distinct()
        print(books)
        if books.exists() :
            return render(request, 'searchresult.html', {'user': user, 'books': books, 'search': search})
        else:
            messages.info(request,"Book not found!")
            return render(request, 'userhome.html',{'user': user})
    else:
        return render(request, 'userhome.html', {'user': user})


@login_required()
def mybooks(request):
    user = request.user
    books = perform_raw_sql("select * from user as U, my_books as MB, book as B where U.User_ID='"+str(user)+"' and U.User_ID=MB.User_ID and MB.ISBN=B.ISBN")
    print(books)
    if len(books)!=0:
        return render(request, 'mybooks.html', {'user': user, 'books': books})
    else:
        messages.info(request,"No Book Added !")
        books={}
        return render(request, 'mybooks.html', {'user': user, 'books': books})


@login_required()
def userhome(request):
    user = request.user
    return render(request, 'userhome.html', {'user':user})


def home(request):
    return render(request,'home.html')


def validatelogin(request):
    djlogout(request)
    if request.method=="POST":
        userid = request.POST.get("username")
        password = request.POST.get("password")
        message = ''

        if LoginCredential.objects.filter(user_id__exact=userid).exists():
            user_cred=LoginCredential.objects.get(user_id=userid)

            if user_cred.password == password:
                print('hello its\n')
                login_user = authenticate(username=userid, password=password)
                djlogin(request, login_user)
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
                new_user = djUser.objects.create_user(
                    username=userid, email="", password=password,
                    first_name="",
                    last_name=""
                )
                user = User.objects.create(user_id = userid ,email_address = email,name = name,house_number = house_no,street = street,locality = locality,postal_code = postal_code,landmark = landmark,city = city,state = state)
                new_credentials = LoginCredential(user=user, password=password)
                new_credentials.save()

            except:
                return print('error')

            message = "no_error"
        return HttpResponse(message)

    else:
        return render(request, 'register.html')
