from django.contrib import admin

# Register your models here.
from . import models

# QQ登陆中间表
admin.site.register(models.OAuthQQUser)