"""广告内容序列化器

date: 18-12-6 下午4:27
"""
from rest_framework.serializers import ModelSerializer

from contents.models import ContentCategory


class ContentCategorySerializersBase(ModelSerializer):
    """广告内容类别序列化器 -- 基类"""
    class Meta:
        """元数据"""
        # 实体类
        model = ContentCategory
        # 字段
        fields = "__all__"


class ContentSerializersBase(ModelSerializer):
    """广告内容序列化器 -- 基类"""
    class Meta:
        """元数据"""
        # 实体类
        model = ContentCategory
        # 字段
        fields = "__all__"
