from django.contrib import admin

from users.models import UserInfo
from books.models import Book

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class BookInline(admin.TabularInline):
	model = Book
	extra = 1

class UserInfoInline(admin.TabularInline):
	model = UserInfo
	max_num = 1
	can_delete = False

class UserAdmin(AuthUserAdmin):
	inlines = [BookInline, UserInfoInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


