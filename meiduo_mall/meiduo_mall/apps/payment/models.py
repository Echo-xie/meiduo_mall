from django.db import models

from meiduo_mall.utils.models import BaseModel
from orders.models import OrderInfo


class Payment(BaseModel):
    """支付结果信息表"""

    # 字段
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='订单')
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="支付宝编号")

    class Meta:
        """元数据"""

        # 数据库表名
        db_table = 'tb_payment'
        # 详细名称
        verbose_name = '支付信息'
        # 详细名称复数
        verbose_name_plural = verbose_name
