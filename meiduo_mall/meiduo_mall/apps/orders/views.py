from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from orders.serializers import CartSKUSerializer2, SaveOrderSerializer
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
            'skus': CartSKUSerializer2(skus, many=True).data
        }
        # 响应数据
        return Response(context)


class OrderAPIView(CreateAPIView):
    """订单操作
    POST orders/action/
    GET orders/action/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SaveOrderSerializer
