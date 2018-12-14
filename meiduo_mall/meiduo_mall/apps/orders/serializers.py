"""订单子应用 -- 序列化器

date: 18-12-11 下午6:45
"""
from django.db import transaction
from django.utils.timezone import now
from django_redis import get_redis_connection
from rest_framework import serializers

from goods.models import SKU
from goods.serializers import SKUSerializerBase
from orders.models import OrderInfo, OrderGoods
from orders.utils import get_orders_goods


class OrderInfoSerializerBase(serializers.ModelSerializer):
    """订单信息序列化器 -- 基类"""

    class Meta:
        """元数据"""

        # 实体类
        model = OrderInfo
        # 字段
        fields = "__all__"


class OrderGoodsSerializerBase(serializers.ModelSerializer):
    """订单商品序列化器 -- 基类"""

    class Meta:
        """元数据"""

        # 实体类
        model = OrderGoods
        # 字段
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品序列化器 -- 基类"""
    sku = SKUSerializerBase()

    class Meta:
        """元数据"""

        # 实体类
        model = OrderGoods
        # 字段
        fields = "__all__"


class OrderInfoSerializer(serializers.ModelSerializer):
    """订单商品序列化器 -- 基类"""
    ordergoods_set = OrderGoodsSerializer(many=True)

    class Meta:
        """元数据"""

        # 实体类
        model = OrderInfo
        # 字段
        fields = "__all__"


class CartSKUSerializer(serializers.ModelSerializer):
    """购物车商品数据序列化器"""

    # 自定义字段
    count = serializers.IntegerField(label='数量')

    class Meta:
        """元数据"""

        # 实体类
        model = SKU
        # 字段
        fields = ('id', 'name', 'default_image_url', 'price', 'count')


class SaveOrderSerializer(serializers.ModelSerializer):
    """保存订单序列化器"""

    class Meta:
        """元数据"""

        # 实体类
        model = OrderInfo
        # 字段
        fields = ('order_id', 'address', 'pay_method')
        # 默认为可写 -- 修改为只读
        read_only_fields = ('order_id',)
        # 字段额外规则
        extra_kwargs = {
            # 地址
            'address': {
                # 只写
                'write_only': True,
                # 必要
                'required': True,
            },
            # 付款方式
            'pay_method': {
                # 只写
                'write_only': True,
                # 必要
                'required': True
            }
        }

    def create(self, validated_data):
        """重写 -- 保存一个订单"""

        # 获取下单用户及请求参数: 地址, 支付方式
        user_ = self.context.get('request').user
        address_ = validated_data.get("address")
        pay_method_ = validated_data.get("pay_method")

        # 生成订单编号 20180704174607000000001 [当前时间戳 + 用户ID]
        order_id = now().strftime('%Y%m%d%H%M%S') + ('%09d' % user_.id)
        # 开启一个事务
        with transaction.atomic():
            # 创建一个保存点
            save_id = transaction.savepoint()
            # 捕获异常
            try:
                # 订单信息表: 保存订单基本信息 (新增一条订单数据)
                order = OrderInfo.objects.create(
                    # 订单ID
                    order_id=order_id,
                    # 下单用户ID
                    user=user_,
                    # 收货地址
                    address=address_,
                    # 支付方式
                    pay_method=pay_method_,
                    # 商品总数量 -- 默认为0, 后面进行计算
                    total_count=0,
                    # 商品总金额 -- 默认为0, 后面进行计算
                    total_amount=0,
                    # 运费 -- 默认10
                    freight=10,
                    # 订单状态 -- 三元表达式
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']  # 支付宝支付: 未付款
                    if pay_method_ == OrderInfo.PAY_METHODS_ENUM['ALIPAY']  # 判断条件: 当前支付方式(货到付款-订单状态未发货, 支付宝支付-订单状态未付款)
                    else OrderInfo.ORDER_STATUS_ENUM['UNSEND'],  # 货到付款：未发货
                )

                # 从Redis中查询购物车商品
                carts = get_orders_goods(request=self.context.get('request'))

                # 下单商品IDs
                sku_ids = carts.keys()
                # 循环所有下单商品IDs
                for sku_id in sku_ids:
                    while True:
                        # 查询sku对象
                        sku = SKU.objects.get(id=sku_id)
                        # 记录原始的库存和销量
                        origin_stock = sku.stock
                        origin_sales = sku.sales

                        # 获取商品购买数量
                        sku_count = carts[sku.id]
                        # 判断库存
                        if sku_count > sku.stock:
                            #
                            raise serializers.ValidationError('库存不足')

                        # 减少库存
                        # sku.stock -= sku_count
                        # 增加销量
                        # sku.sales += sku_count
                        # 保存具体商品信息
                        # sku.save()

                        # 使用乐观锁修改库存和销量
                        new_stock = origin_stock - sku_count
                        new_sales = origin_sales + sku_count
                        # 根据具体商品ID和原始库存获取信息, 然后进行修改 -- 如果获取不到信息, 则表示此条商品信息被操作
                        count = SKU.objects.filter(id=sku.id, stock=origin_stock).update(stock=new_stock, sales=new_sales)
                        # 如果操作结果为0 -- 表示数据修改操作失败, 因为此商品信息被已其他事务操作
                        if count == 0:
                            # 处理: 重新查询、判断、修改商品库存, 直到成功或因库存不足退出
                            print('---重新查询、判断、修改商品库存--', origin_stock)
                            #
                            continue

                        # 修改SPU销量
                        sku.goods.sales += sku_count
                        # 保存商品信息
                        sku.goods.save()

                        # 订单商品表: 保存订单商品信息
                        OrderGoods.objects.create(
                            # 订单信息
                            order=order,
                            # 具体商品信息
                            sku=sku,
                            # 具体商品购买数量
                            count=sku_count,
                            # 具体商品购买单价
                            price=sku.price
                        )

                        # 累加订单信息中的商品总数量和总金额
                        order.total_count += sku_count
                        order.total_amount += (sku_count * sku.price)
                        # 表示一个订单商品保存成功, 需要跳出while死循环, 继续保存下一个订单商品
                        break

                # 循环完之后购物总金额 + 加入运费
                order.total_amount += order.freight
                # 订单信息保存
                order.save()
            # 处理异常
            except Exception as e:
                # 回滚到保存点
                transaction.savepoint_rollback(save_id)
                print('下单失败', e)
                raise e
            # 提交事务
            transaction.savepoint_commit(save_id)
            # 数据库连接
            redis_conn = get_redis_connection('carts')
            # 购物车商品勾选信息 -- 只有勾选中的购物车商品才会结算
            selected_sku_ids = redis_conn.smembers('cart_selected_%s' % user_.id)
            # 获取管道
            pl = redis_conn.pipeline()
            # 清除购物车中已结算的商品 -- 根据购物车商品勾选信息, 删除购物车商品和勾选信息
            pl.hdel('cart_%s' % user_.id, *selected_sku_ids)
            pl.srem('cart_selected_%s' % user_.id, *selected_sku_ids)
            # 管道执行
            pl.execute()

            # 返回新创建的订单对象
            return order
