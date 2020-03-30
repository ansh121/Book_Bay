# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Book(models.Model):
    isbn = models.CharField(db_column='ISBN', primary_key=True, max_length=13)  # Field name made lowercase.
    book_name = models.TextField(db_column='Book_Name')  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    author = models.TextField(db_column='Author', blank=True, null=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book'


class BookReview(models.Model):
    rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
    review = models.TextField(db_column='Review', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='ISBN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book_review'
        unique_together = (('user', 'isbn'),)


class History(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='ISBN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'history'
        unique_together = (('user', 'isbn'),)


class LoginCredential(models.Model):
    password = models.CharField(db_column='Password', max_length=30)  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_credential'


class MyBooks(models.Model):
    repayment_policy = models.TextField(db_column='Repayment_Policy')  # Field name made lowercase.
    availability = models.IntegerField(db_column='Availability')  # Field name made lowercase.
    other_specifications = models.TextField(db_column='Other_Specifications', blank=True, null=True)  # Field name made lowercase.
    security_money_of_book = models.IntegerField(db_column='Security_Money_of_Book')  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_ID', primary_key=True)  # Field name made lowercase.
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='ISBN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'my_books'
        unique_together = (('user', 'isbn'),)


class Request(models.Model):
    date_of_request = models.DateTimeField(db_column='Date_of_Request')  # Field name made lowercase.
    request_message = models.TextField(db_column='Request_Message', blank=True, null=True)  # Field name made lowercase.
    request_id = models.AutoField(db_column='Request_ID', primary_key=True)  # Field name made lowercase.
    borrow_time_duration = models.IntegerField()
    completion_flag = models.IntegerField()
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='ISBN')  # Field name made lowercase.
    requested_user = models.ForeignKey('User', models.DO_NOTHING, db_column='Requested_User_ID', related_name= 'Requested_User_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'request'


class User(models.Model):
    user_id = models.CharField(db_column='User_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    email_address = models.CharField(db_column='Email_Address', max_length=40)  # Field name made lowercase.
    house_number = models.CharField(db_column='House_Number', max_length=10, blank=True, null=True)  # Field name made lowercase.
    street = models.TextField(db_column='Street')  # Field name made lowercase.
    locality = models.TextField(db_column='Locality')  # Field name made lowercase.
    postal_code = models.DecimalField(db_column='Postal_Code', max_digits=6, decimal_places=0)  # Field name made lowercase.
    landmark = models.TextField(db_column='Landmark', blank=True, null=True)  # Field name made lowercase.
    city = models.TextField(db_column='City')  # Field name made lowercase.
    state = models.TextField(db_column='State')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'


class UserPhoneNumber(models.Model):
    phone_number = models.DecimalField(db_column='Phone_Number', primary_key=True, max_digits=10, decimal_places=0)  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    is_primary = models.IntegerField(db_column='Is_Primary')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_phone_number'
        unique_together = (('phone_number', 'user'),)
