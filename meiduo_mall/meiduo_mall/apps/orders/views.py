from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from orders.models import OrderInfo
from orders.serializers import CartSKUSerializer, SaveOrderSerializer, OrderInfoSerializer, OrderGoodsSerializer
from orders.utils import get_orders_goods


class OrderSettlementView(APIView):
    """订单结算
    GET orders/settlement/
    """

    # 用户验证
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取订单商品信息"""

        # 获取下单商品
        cart = get_orders_goods(request=request)

        # 查询下单商品的所有商品信息
        skus = SKU.objects.filter(id__in=cart.keys())
        # 循环所有下单商品信息
        for sku in skus:
            # 给每一个商品sku对象补充上 count 数量
            sku.count = cart[sku.id]

        # 手动响应的字典数据
        context = {
            # 运费
            'freight': 10.0,
            # 序列化下单商品信息, many=True 多条数据序列化开启
            'skus': CartSKUSerializer(skus, many=True).data
        }
        # 响应数据
        return Response(context)


class OrderAPIView(CreateAPIView, ListAPIView):
    """订单操作
    POST orders/action/
    GET orders/action/
    """

    # 用户验证
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """获取序列化器"""

        # post请求
        if self.request.method == "POST":
            return SaveOrderSerializer
        # get请求
        elif self.request.method == "GET":
            return OrderInfoSerializer

        return None

    # 查询集
    # queryset = OrderInfo.objects.all()

    def get_queryset(self):
        order_info = OrderInfo.objects.order_by("create_time").all()
        # for order in order_info:
        #     order.goods = OrderGoodsSerializer(order.skus.all(), many=True).data
        return order_info

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     order_list = response.data.all()
    #     for order in order_list:
    #         order.skus
    #     return response
