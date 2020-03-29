from django.contrib import admin
from bookbayapp.models import *

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookReview)
admin.site.register(LoginCredential)
admin.site.register(Request)
admin.site.register(MyBooks)
admin.site.register(UserPhoneNumber)
admin.site.register(History)