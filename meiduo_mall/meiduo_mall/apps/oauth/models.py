from django.db import models

from meiduo_mall.utils.models import BaseModel


class OAuthQQUser(BaseModel):
    """关系映射表
    QQ号(openid)与美多用户的关系映射表

    """
    # 美多用户
    user = models.ForeignKey('users.User', verbose_name='用户')
    # qq用户
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        """元数据"""
        # 数据库表名
        db_table = 'tb_oauth_qq'
        # 详情名称
        verbose_name = 'QQ登录用户数据'
        # 详情名称复数
        verbose_name_plural = verbose_name
