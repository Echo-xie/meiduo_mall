from django.contrib import admin

# Register your models here.
from . import models

# 用户站点
admin.site.register(models.User)
# 用户地址站点
admin.site.register(models.Address)