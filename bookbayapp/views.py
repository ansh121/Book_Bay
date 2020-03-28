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

from datetime import datetime


def execute_only_raw_sql(sql):
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        return True
    except:
        return False


def perform_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
    except:
        print('error in sql')
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
def history(request):
    user = request.user
    try:
        incomingrequests=perform_raw_sql("select * from my_books as MB, request as R, user as U, User as RU, book as B where MB.ISBN=B.ISBN and B.ISBN=R.ISBN and R.Requested_User_ID='"+str(user)+"' and R.User_ID=RU.User_ID and U.User_ID=R.Requested_User_ID and R.completion_flag <> "+str(0)+" order by R.ISBN")
        outgoingrequests=perform_raw_sql("select * from my_books as MB, request as R, user as U, User as RU, book as B where MB.ISBN=B.ISBN and B.ISBN=R.ISBN and R.User_ID='"+str(user)+"' and R.Requested_User_ID=RU.User_ID and U.User_ID=R.User_ID and R.completion_flag <> "+str(0)+" order by R.ISBN")
        dict={}
        dict['incomingrequests']=incomingrequests
        dict['outgoingrequests']=outgoingrequests
        dict['user']=user
        print(incomingrequests)
        print(outgoingrequests)
        return render(request, 'history.html', dict)
    except:
        print('Error in Pending Request!')
        return render(request, 'history.html', {'user': user})


@login_required()
def pendingrequest(request):
    user = request.user
    if request.POST.get("decline"):
        requestid=request.POST.get("requestid")
        bool=execute_only_raw_sql("UPDATE request SET completion_flag=-2 WHERE Request_ID = "+str(requestid))

    if request.POST.get("cancel"):
        requestid = request.POST.get("requestid")
        bool=execute_only_raw_sql("UPDATE request SET completion_flag=-1 WHERE Request_ID = "+str(requestid))

    if request.POST.get("accept"):
        requestid = request.POST.get("requestid")
        bool=execute_only_raw_sql("UPDATE request SET completion_flag=1 WHERE Request_ID = "+str(requestid))
        req = Request.objects.get(request_id=requestid)
        bool=bool and execute_only_raw_sql("UPDATE my_books SET Avaliability = 0 WHERE ISBN='"+str(req.isbn)+"' and User_ID = '"+str(req.requesteduser)+"'")
        print(bool)

    try:
        incomingrequests=perform_raw_sql("select * from my_books as MB, request as R, user as U, User as RU, book as B where MB.ISBN=B.ISBN and B.ISBN=R.ISBN and R.Requested_User_ID='"+str(user)+"' and R.User_ID=RU.User_ID and U.User_ID=R.Requested_User_ID and R.completion_flag="+str(0)+" order by R.ISBN")
        outgoingrequests=perform_raw_sql("select * from my_books as MB, request as R, user as U, User as RU, book as B where MB.ISBN=B.ISBN and B.ISBN=R.ISBN and R.User_ID='"+str(user)+"' and R.Requested_User_ID=RU.User_ID and U.User_ID=R.User_ID and R.completion_flag="+str(0)+" order by R.ISBN")
        dict={}
        dict['incomingrequests']=incomingrequests
        dict['outgoingrequests']=outgoingrequests
        dict['user']=user
        print(incomingrequests)
        print(outgoingrequests)
        return render(request, 'pendingrequest.html', dict)
    except:
        print('Error in Pending Request!')
        return render(request, 'pendingrequest.html', {'user': user})


@login_required()
def bookdetail(request):
    user = request.user

    if request.POST.get("addreview"):
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        isbn = request.POST.get("isbn")
        already_exist=BookReview.objects.filter(user=User.objects.get(user_id=user),isbn=Book.objects.get(isbn=isbn))
        if already_exist.exists():
            BookReview.objects.update(rating=rating,review=review,user=User.objects.get(user_id=user),isbn=Book.objects.get(isbn=isbn))
        else:
            BookReview.objects.create(rating=rating, review=review, user=User.objects.get(user_id=user),isbn=Book.objects.get(isbn=isbn))
        print("Review Added/Updated Successfully")
        messages.success(request,"Review Added/Updated Successfully")

    if request.POST.get("makerequest"):
        borrowduration=request.POST.get("borrowduration")
        message=request.POST.get("message")
        isbn=request.POST.get("isbn")
        requesteduserid=request.POST.get("ownerid")
        date=datetime.today()
        complete=0

        already_requested=Request.objects.filter(user=User.objects.get(user_id=user),isbn=Book.objects.get(isbn=isbn),requesteduser=User.objects.get(user_id=requesteduserid))
        if already_requested.count() != 0:
            messages.info(request,"Book already requested from the user, please delete previous requests to make another one.")
            print("Book already requested")
        else:
            Request.objects.create(borrow_time_duration=borrowduration,date_of_request=date,request_message=message,completion_flag=complete,user=User.objects.get(user_id=user),isbn=Book.objects.get(isbn=isbn),requesteduser=User.objects.get(user_id=requesteduserid))
            messages.success(request,"Book Request Submitted Successfully")
            print("Book Request Successful")

    try:
        isbn=request.POST.get("isbn")
        book=Book.objects.get(isbn=isbn)
        print(book)

        users=perform_raw_sql("select * from my_books as MB, user as U where U.User_Id=MB.User_ID and MB.ISBN='"+str(isbn)+"'")
        reviews=perform_raw_sql("select * from book_review as BR, user as U where BR.ISBN='"+str(isbn)+"' and BR.User_ID=U.User_ID")
        dict={}
        dict['users']=users
        print(dict)
        dict['book']=book
        dict['user']=user
        dict['reviews']=reviews
        print(reviews)
        return render(request, 'bookdetail.html', dict)
    except:
        return render(request, 'bookdetail.html', {'user': user})

@login_required()
def myaccount(request):
    userid = request.user

    if request.POST.get("changepassword"):
        oldpass=request.POST.get("oldpassword")
        newpass=request.POST.get("newpassword")
        confnewpass=request.POST.get("confirmnewpassword")

        logcred=LoginCredential.objects.get(user=User.objects.get(user_id=userid))
        if logcred.password==oldpass :
            if newpass==confnewpass :
                logcred.password=newpass
                logcred.save()
                messages.success(request,'Password updated successfully')
            else:
                messages.info(request,'Password did not match')
        else:
            messages.info(request,'Incorrect Password !')

    if request.POST.get("editdetails"):
        email = request.POST.get("email")
        name = request.POST.get("name")
        house_no = request.POST.get("house_no")
        street = request.POST.get("street")
        locality = request.POST.get("locality")
        postal_code = request.POST.get("postal_code")
        landmark = request.POST.get("landmark")
        city = request.POST.get("city")
        state = request.POST.get("state")

        try:
            u=User.objects.get(user_id=userid)
            u.email_address = email
            u.name = name
            u.house_number = house_no
            u.street = street
            u.locality = locality
            u.postal_code = postal_code
            u.landmark = landmark
            u.city = city
            u.state = state
            u.save()
            print("User details updated successfully")
        except:
            print("User details update error")

    userdetail = perform_raw_sql("select * from user as U, login_credential as LC where U.User_ID='" + str(userid) + "' and U.User_ID=LC.User_ID")
    userdetail = userdetail[0]
    userdetail['user'] = userid
    print(userdetail)
    return render(request, 'myaccount.html', userdetail)


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
    if request.POST.get("delete"):
        delete_isbn=request.POST.get('isbn')
        flag=execute_only_raw_sql("delete from my_books as MB where MB.User_ID='"+str(user)+"' and MB.ISBN="+str(delete_isbn))
        if flag==False:
            print('Error in delete : ',delete_isbn)
        else:
            print('Deleted isbn: ', delete_isbn, ' from user:',user)

    if request.POST.get("addbook"):
        bookname=request.POST.get('title')
        genre=request.POST.get('genre')
        author=request.POST.get('author')
        edition=request.POST.get('edition')
        isbn=request.POST.get('isbn')
        availability=request.POST.get('availability')
        repaypol=request.POST.get('repaymentpolicy')
        otherspec=request.POST.get('otherspecification')
        securitymoney=request.POST.get('securitymoneyofbook')

        print(genre)
        try:
            Book.objects.create(isbn=isbn,book_name=bookname,edition=int(edition),author=author,genre=genre)
            print("new book added")
        except:
            print("book already exists")

        try:
            MyBooks.objects.create(repayment_policy=repaypol, availability=int(availability),
                                   other_specifications=otherspec,
                                   security_money_of_book=int(securitymoney), user=User.objects.get(user_id=user),
                                   isbn=Book.objects.get(isbn=isbn))
            print("new book added to user : ", user)
        except:
            messages.info(request,"Book already exists !")
            print("Error in adding Book")

    if request.POST.get("editbook"):
        bookname = request.POST.get('title')
        genre = request.POST.get('genre')
        author = request.POST.get('author')
        edition = request.POST.get('edition')
        isbn = request.POST.get('isbn')
        availability = request.POST.get('availability')
        repaypol = request.POST.get('repaymentpolicy')
        otherspec = request.POST.get('otherspecification')
        securitymoney = request.POST.get('securitymoneyofbook')

        try:
            b=Book.objects.get(isbn=isbn)
            b.edition=int(edition)
            b.author=author
            b.genre=genre
            b.save()

            mb=MyBooks.objects.get(isbn=isbn, user=user)
            mb.repayment_policy = repaypol
            mb.availability = int(availability)
            mb.other_specifications = otherspec
            mb.security_money_of_book = int(securitymoney)
            mb.save()
            print("book updated")
        except:
            print("book update error")


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
