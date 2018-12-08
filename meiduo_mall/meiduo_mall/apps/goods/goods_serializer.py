"""商品序列化器

date: 18-12-6 下午4:32
"""
from rest_framework.serializers import ModelSerializer

from goods.models import GoodsCategory, SKUSpecification, GoodsChannel, Brand, Goods, GoodsSpecification, SpecificationOption, SKU, SKUImage


class GoodsCategorySerializerBase(ModelSerializer):
    """商品类别序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = GoodsCategory
        # 字段
        fields = "__all__"


class GoodsChannelSerializerBase(ModelSerializer):
    """商品频道序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = GoodsChannel
        # 字段
        fields = "__all__"


class BrandSerializerBase(ModelSerializer):
    """品牌序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = Brand
        # 字段
        fields = "__all__"


class GoodsSerializerBase(ModelSerializer):
    """商品SPU序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = Goods
        # 字段
        fields = "__all__"


class GoodsSpecificationSerializerBase(ModelSerializer):
    """商品规格序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = GoodsSpecification
        # 字段
        fields = "__all__"


class SpecificationOptionSerializerBase(ModelSerializer):
    """规格选项序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = SpecificationOption
        # 字段
        fields = "__all__"


class SKUSerializerBase(ModelSerializer):
    """商品SKU序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = SKU
        # 字段
        fields = "__all__"


class SKUImageSerializerBase(ModelSerializer):
    """SKU图片序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = SKUImage
        # 字段
        fields = "__all__"


class SKUSpecificationSerializerBase(ModelSerializer):
    """SKU具体规格序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 实体类
        model = SKUSpecification
        # 字段
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    """类别序列化器"""

    class Meta:
        """元数据"""
        # 实体类
        model = GoodsCategory
        # 字段
        fields = ('id', 'name')


class ChannelSerializer(ModelSerializer):
    """频道序列化器"""
    category = CategorySerializer()

    class Meta:
        """元数据"""
        # 实体类
        model = GoodsChannel
        # 字段
        fields = ('category', 'url')


class SKUSerializer(ModelSerializer):
    """序列化器序输出商品SKU信息"""

    class Meta:
        """元数据"""
        # 实体类
        model = SKU
        # 字段
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')
