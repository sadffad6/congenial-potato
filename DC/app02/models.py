from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class NameToUser(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    username=models.CharField(max_length=100,default='默认名字')
class OnlineUser(models.Model):
    username = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    name=models.CharField(max_length=32)