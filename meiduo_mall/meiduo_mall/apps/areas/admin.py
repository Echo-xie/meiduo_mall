from django.contrib import admin

# Register your models here.
from areas import models

# 省市区管理站点
admin.site.register(models.Area)