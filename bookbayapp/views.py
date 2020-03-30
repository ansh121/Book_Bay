from django.shortcuts import render
from bookbayapp.models import *
from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as djUser

from django.contrib import messages
from django.db import connection

from datetime import datetime

from isbnlib import meta
from isbnlib.config import add_apikey

import os

try:
    proxy = 'http://172.16.2.30:8080'
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    os.environ['NO_PROXY'] = 'localhost,127.0.0.1/*,127.0.0.1'
except:
    print("proxy error")


def execute_only_raw_sql(sql):
    print('sql - ', sql)
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


def contact(request):
    if request.user.is_authenticated:
        return render (request,'logincontact.html')
    else:
        return render (request,'contact.html')

def about(request):
    if request.user.is_authenticated:
        return render (request,'loginabout.html')
    else:
        return render (request,'about.html')



@login_required()
def history(request):
    user = request.user
    try:
        incomingrequests=perform_raw_sql("select * from my_books as MB, request as R, user as U, user as RU, book as B where MB.ISBN=B.ISBN and B.ISBN=R.ISBN and R.Requested_User_ID='"+str(user)+"' and R.User_ID=RU.User_ID and U.User_ID=R.Requested_User_ID order by R.Date_of_Request")
        outgoingrequests=perform_raw_sql("select * from my_books as MB, request as R, user as U, user as RU, book as B where MB.ISBN=B.ISBN and B.ISBN=R.ISBN and R.User_ID='"+str(user)+"' and R.Requested_User_ID=RU.User_ID and U.User_ID=R.User_ID order by R.Date_of_Request")
        dict={}
        dict['incomingrequests']=incomingrequests
        dict['outgoingrequests']=outgoingrequests
        dict['user']=user
        for req in incomingrequests:
            numbers = perform_raw_sql("select p.Phone_Number from user_phone_number as p where p.User_ID='"+str(req['User_ID'])+"'")
            l = []
            for p in numbers:
                l.append(p['Phone_Number'])
            req['Phone_Numbers']=l
        print(incomingrequests)
        for req in outgoingrequests:
            numbers = perform_raw_sql("select p.Phone_Number from user_phone_number as p where p.User_ID='"+str(req['User_ID'])+"'")
            l = []
            for p in numbers:
                l.append(p['Phone_Number'])
            req['Phone_Numbers']=l
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
        req=perform_raw_sql("SELECT * from request as r where r.Request_ID ="+str(requestid))
        bool=bool and execute_only_raw_sql("UPDATE my_books SET Availability = 0 WHERE ISBN='"+str(req[0]['ISBN'])+"' and User_ID = '"+str(user)+"'")
        print(bool)

    try:
        incomingrequests=perform_raw_sql("select * from my_books as MB, request as R, user as U, user as RU, book as B where MB.ISBN=B.ISBN and B.ISBN=R.ISBN and R.Requested_User_ID='"+str(user)+"' and R.User_ID=RU.User_ID and U.User_ID=R.Requested_User_ID and R.completion_flag="+str(0)+" order by R.ISBN")
        outgoingrequests=perform_raw_sql("select * from my_books as MB, request as R, user as U, user as RU, book as B where MB.ISBN=B.ISBN and B.ISBN=R.ISBN and R.User_ID='"+str(user)+"' and R.Requested_User_ID=RU.User_ID and U.User_ID=R.User_ID and R.completion_flag="+str(0)+" order by R.ISBN")
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

        already_requested=Request.objects.filter(user=User.objects.get(user_id=user),isbn=Book.objects.get(isbn=isbn),requested_user=User.objects.get(user_id=requesteduserid), completion_flag=0)
        if already_requested.count() != 0:
            messages.info(request,"Book already requested from the user, please delete previous requests to make another one.")
            print("Book already requested")
        else:
            Request.objects.create(borrow_time_duration=borrowduration,date_of_request=date,request_message=message,completion_flag=complete,user=User.objects.get(user_id=user),isbn=Book.objects.get(isbn=isbn),requested_user=User.objects.get(user_id=requesteduserid))
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

    if request.POST.get("removenumber"):
        number = request.POST.get("phone")
        flag = execute_only_raw_sql("DELETE from user_phone_number as p where p.User_ID='"+str(userid)+"' and p.Phone_Number='"+str(number)+"'")
        print('phone number delition - ',flag)

    if request.POST.get("addphoneno"):
        newno=request.POST.get("phoneno")
        password = request.POST.get("password")

        logcred = LoginCredential.objects.get(user=User.objects.get(user_id=userid))
        if logcred.password == password:
            alreadyexist = perform_raw_sql("select p.Phone_Number from user_phone_number as p where p.User_ID='"+str(userid)+"'")
            l = []
            for p in alreadyexist:
                l.append(p['Phone_Number'])
            if newno in l:
                messages.info(request,"Number Already Exists !")
            else:
                contact = UserPhoneNumber.objects.create(user=User.objects.get(user_id=userid), phone_number=newno, isprimary=0)
                contact.save()
                messages.success(request,"Mobile No added successfully")

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
    phonenoprimary = perform_raw_sql("select upn.Phone_Number from user_phone_number as upn where upn.User_ID='"+str(userid)+"' and Is_Primary=1")
    phonenosecondary = perform_raw_sql("select upn.Phone_Number from user_phone_number as upn where upn.User_ID='" + str(userid) + "' and Is_Primary=0")
    print(phonenoprimary, phonenosecondary)
    userdetail['user'] = userid
    userdetail['phonenoprimary']=phonenoprimary[0]['Phone_Number']
    l = []
    for p in phonenosecondary:
        l.append(p['Phone_Number'])
    userdetail['phonenosecondary'] = l
    print(userdetail)
    return render(request, 'myaccount.html', userdetail)


@login_required()
def searchresult(request):
    user = request.user
    if request.method=="POST":
        search = request.POST.get('search')
        print(search)
        namebooks = Book.objects.filter(book_name__icontains=search)
        isbnbooks = Book.objects.filter(isbn__icontains=search)
        authbooks = Book.objects.filter(author__icontains=search)
        books = namebooks | isbnbooks | authbooks
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

    if request.POST.get("changeavailable"):
        availability=request.POST.get("available")
        isbn = request.POST.get('isbn')
        bool=execute_only_raw_sql("UPDATE my_books SET Availability="+str(availability)+" where User_ID='"+str(user)+"' and ISBN='"+str(isbn)+"'")
        print(bool)
        messages.success(request,"Availability Changed Successfully !!!")

    if request.POST.get("delete"):
        delete_isbn=request.POST.get('isbn')
        flag=execute_only_raw_sql("delete from my_books as MB where MB.User_ID='"+str(user)+"' and MB.ISBN='"+str(delete_isbn)+"'")
        if flag==False:
            print('Error in delete : ',delete_isbn)
        else:
            print('Deleted isbn: ', delete_isbn, ' from user:',user)

    if request.POST.get("addbook"):
        isbn=request.POST.get('isbn')
        availability=request.POST.get('availability')
        repaypol=request.POST.get('repaymentpolicy')
        otherspec=request.POST.get('otherspecifications')
        securitymoney=request.POST.get('securitymoneyofbook')

        SERVICE = 'isbndb'
        APIKEY = 'temp475675837'  # <-- replace with YOUR key
        # register your key
        add_apikey(SERVICE, APIKEY)
        try:
            book=meta(isbn)
            print(book)
            try:
                auth=""
                for a in book['Authors']:
                    auth=auth+','+a
                auth=auth[1:]
                try:
                    year=int(book['Year'])
                except:
                    year=None

                if book['Language'] == "":
                    lang=None
                else:
                    lang=book['Language']

                Book.objects.create(isbn=isbn, book_name=book['Title'],author=auth,language= lang,year=year )
                print("new book added")

            except Exception as e:
                print(e)
                print("book already exists")

            try:
                MyBooks.objects.create(repayment_policy=repaypol, availability=int(availability),
                                       other_specifications=otherspec,
                                       security_money_of_book=int(securitymoney), user=User.objects.get(user_id=user),
                                       isbn=Book.objects.get(isbn=isbn))
                messages.success(request, "Book Added Successfully !!!")
                print("new book added to user : ", user)
            except Exception as e:
                print(e)
                messages.info(request, "Book already exists !")
                print("Error in adding Book")
        except Exception as e:
            print(e)
            messages.ERROR(request,"Wrong ISBN Entered !!!")


    if request.POST.get("editbook"):
        isbn = request.POST.get('isbn')
        availability = request.POST.get('availability')
        repaypol = request.POST.get('repaymentpolicy')
        otherspec = request.POST.get('otherspecification')
        securitymoney = request.POST.get('securitymoneyofbook')

        try:
            mb = MyBooks.objects.get(isbn=isbn, user=User.objects.get(user_id=user))
            mb.repayment_policy = repaypol
            mb.availability = int(availability)
            mb.other_specifications = otherspec
            mb.security_money_of_book = int(securitymoney)
            mb.save()
            print("book updated")
        except Exception as e:
            print(e)
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
    djlogout(request)
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
    djlogout(request)
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
        mobileno = request.POST.get("mobileno")
        password = request.POST.get("password")

        message=""
        if User.objects.filter(user_id__exact=userid).exists():
            message = 'name_taken'

        elif User.objects.filter(email_address__exact=email).exists():
            message = 'email_taken'

        if not message:
            try:
                user = User.objects.create(user_id=userid, email_address=email, name=name, house_number=house_no,
                                           street=street, locality=locality, postal_code=postal_code, landmark=landmark,
                                           city=city, state=state)

                new_user = djUser.objects.create_user(
                    username=userid, email="", password=password,
                    first_name="",
                    last_name=""
                )
                b=execute_only_raw_sql("insert into login_credential(User_ID,Password) values('"+str(userid)+"','"+str(password)+"')")
                print(b)
                contact = UserPhoneNumber.objects.create(user=user,phone_number=mobileno,isprimary=1)
                contact.save()

            except Exception as e:
                print(e)
                return print('error')

            message = "no_error"
        return HttpResponse(message)

    else:
        return render(request, 'register.html')


