from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=20, verbose_name='名称')
    # 自关联(特殊的一对多): 生成的字段名 parent_id
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上级行政区划')

    class Meta:
        """元数据"""
        # 数据库表名
        db_table = 'tb_areas'
        # 详情名称
        verbose_name = '行政区划'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
