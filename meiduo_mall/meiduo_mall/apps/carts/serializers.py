"""购物车子应用序列化器

date: 18-12-10 下午3:08
"""
from rest_framework import serializers

from goods.models import SKU


class CartSerializer(serializers.Serializer):
    """购物车数据序列化器"""

    # 自定义字段
    sku_id = serializers.IntegerField(label='sku id ', min_value=1, required=True)
    count = serializers.IntegerField(label='数量', min_value=1, required=True)
    selected = serializers.BooleanField(label='是否勾选', default=True)

    def validate(self, attrs):
        """自定义校验

        :param attrs: 需要校验的数据
        :return: 校验成功后的数据
        """
        try:
            # 访问数据库获取数据, 判断此sku_id是否存在
            sku = SKU.objects.get(id=attrs.get('sku_id'))
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        # 返回验证成功后的数据
        return attrs


class CartSKUSerializer(serializers.ModelSerializer):
    """购物车商品数据序列化器"""

    # 自定义字段
    count = serializers.IntegerField(label='数量')
    selected = serializers.BooleanField(label='是否勾选')

    class Meta:
        """元数据"""

        # 实体类
        model = SKU
        # 字段
        fields = ('id', 'name', 'default_image_url', 'price', 'count', 'selected')


class CartDeleteSerializer(serializers.Serializer):
    """删除购物车数据序列化器"""

    # 自定义字段
    sku_id = serializers.IntegerField(label='商品id', min_value=1)

    def validate(self, attrs):
        """自定义校验

        :param attrs: 需要校验的数据
        :return: 校验成功后的数据
        """
        try:
            # 访问数据库获取数据, 判断此sku_id是否存在
            sku = SKU.objects.get(id=attrs.get('sku_id'))
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        # 返回验证成功后的数据
        return attrs
