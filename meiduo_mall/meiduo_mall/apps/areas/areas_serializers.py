"""

date: 18-12-5 下午9:33
"""
from rest_framework.serializers import ModelSerializer

from areas.models import Area


class AreaSerializerBase(ModelSerializer):
    """省市区管理序列化器 -- 基类

    """

    class Meta:
        """元数据"""
        # 实体类
        model = Area
        # 字段
        fields = "__all__"


class AreaSerializer(AreaSerializerBase):
    """地址详情序列化器

    """

    class Meta:
        """元数据"""
        # 实体类
        model = Area
        # 字段
        fields = ('id', 'name')
