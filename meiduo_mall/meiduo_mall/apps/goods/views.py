from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from goods.models import GoodsCategory, SKU
from goods.serializers import ChannelSerializer, CategorySerializer, SKUSerializer, SKUIndexSerializer


class CategoryView(GenericAPIView):
    """商品列表页面包屑导航
    GET /categories/(?P<pk>\d+)/
    """

    # 查询集 -- 所有商品类别
    queryset = GoodsCategory.objects.all()

    def get(self, request, pk=None):
        """获取面包屑导航"""

        # 返回数据字典
        ret = {
            # 一级类别
            'cat1': '',
            # 二级类别
            'cat2': '',
            # 三级类别
            'cat3': '',
        }

        # 当前商品类别
        category = self.get_object()

        # 如果商品类别没有父类 -- [一级类别]
        if category.parent is None:
            # 通过 频道 查询 类别：  category.goodschannel_set.all()[0]
            # 设置[一级类别]数据
            ret['cat1'] = ChannelSerializer(category.goodschannel_set.all()[0]).data
        # 如果当前商品类别没有子类别 -- [三级类别]
        elif category.goodscategory_set.count() == 0:
            # 设置[三级类别]数据
            ret['cat3'] = CategorySerializer(category).data
            # 获取[二级类别]数据
            cat2 = category.parent
            # 设置[二级类别]数据
            ret['cat2'] = CategorySerializer(cat2).data
            # 设置[一级类别]数据
            ret['cat1'] = ChannelSerializer(cat2.parent.goodschannel_set.all()[0]).data
        # 否则 -- [二级类别]
        else:
            # 设置[二级类别]数据
            ret['cat2'] = CategorySerializer(category).data
            # 设置[一级类别]数据
            ret['cat1'] = ChannelSerializer(category.parent.goodschannel_set.all()[0]).data

        # 返回封装好的数据
        return Response(ret)


class SKUListView(ListAPIView):
    """查询商品列表数据
    GET /goods/skus_list/
    """

    # 序列化器
    serializer_class = SKUSerializer
    # 查询集 -- 只查询上架商品
    queryset = SKU.objects.filter(is_launched=True)

    # 配置排序和过滤的管理类 [OrderingFilter: 排序, DjangoFilterBackend: 过滤]
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    # 排序字段 (创建时间, 价格, 人气)
    ordering_fields = ('create_time', 'price', 'sales')
    # 过滤字段 (类别)
    filter_fields = ('category',)


class SKUSearchViewSet(HaystackViewSet):
    """SKU搜索视图集
    HaystackViewSet： 查一条，查多条
    GET /goods/skus_search/
    """
    # 索引实体类
    index_models = [SKU]
    # 序列化器
    serializer_class = SKUIndexSerializer
