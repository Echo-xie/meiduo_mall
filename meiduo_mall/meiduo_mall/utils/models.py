"""实体类基类

date: 18-12-5 下午3:20
"""
from django.db import models


class BaseModel(models.Model):
    """实体类基类"""
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 更新时间
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        """元数据"""
        # abstract: 抽象
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True
