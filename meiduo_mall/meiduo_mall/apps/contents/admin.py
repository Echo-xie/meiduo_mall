from django.contrib import admin

from . import models

# 广告内容类别
admin.site.register(models.ContentCategory)
# 广告内容
admin.site.register(models.Content)
