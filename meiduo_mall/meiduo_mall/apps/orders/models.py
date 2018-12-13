from django.db import models
from meiduo_mall.utils.models import BaseModel
from users.models import User, Address
from goods.models import SKU


class OrderInfo(BaseModel):
    """订单信息"""

    # 支付选项 -- 数据
    PAY_METHODS_ENUM = {
        # 货到付款
        "CASH": 1,
        # 阿里支付
        "ALIPAY": 2
    }

    # 订单状态 -- 数据
    ORDER_STATUS_ENUM = {
        # 未支付
        "UNPAID": 1,
        # 未发货
        "UNSEND": 2,
        # 未收货
        "UNRECEIVED": 3,
        # 未评论
        "UNCOMMENT": 4,
        # 已完成
        "FINISHED": 5
    }

    # 支付选项 -- 字段选项
    PAY_METHOD_CHOICES = (
        (1, "货到付款"),
        (2, "支付宝"),
    )

    # 订单状态 -- 字段选项
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
        (6, "已取消"),
    )
    # 自定义字段
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单号")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="下单用户")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="收获地址")
    total_count = models.IntegerField(default=1, verbose_name="商品总数")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总金额")
    freight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="运费")
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式")
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态")

    class Meta:
        """元数据"""
        # 数据库表名
        db_table = "tb_order_info"
        # 详细名称
        verbose_name = '订单基本信息'
        # 详细名称复数
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """ 订单商品 """
    # 满意度评分 -- 字段选项
    SCORE_CHOICES = (
        (0, '0分'),
        (1, '20分'),
        (2, '40分'),
        (3, '60分'),
        (4, '80分'),
        (5, '100分'),
    )
    # 自定义字段
    order = models.ForeignKey(OrderInfo, related_name='skus', on_delete=models.CASCADE, verbose_name="订单")
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT, verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    comment = models.TextField(default="", verbose_name="评价信息")
    score = models.SmallIntegerField(choices=SCORE_CHOICES, default=5, verbose_name='满意度评分')
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名评价')
    is_commented = models.BooleanField(default=False, verbose_name='是否评价了')

    class Meta:
        """元数据"""
        # 数据库表名
        db_table = "tb_order_goods"
        # 详细名称
        verbose_name = '订单商品'
        # 详细名称复数
        verbose_name_plural = verbose_name
