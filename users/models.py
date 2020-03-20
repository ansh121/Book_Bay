from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User)
	address = models.CharField(max_length = 200)
	dob = models.DateField()