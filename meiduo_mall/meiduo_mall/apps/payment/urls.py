"""付款子应用路由

date: 18-12-14 下午6:51
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # 获取阿里支付url -- GET
    url(r"^alipay/(?P<order_id>\d+)/$", views.AliPaymentView.as_view()),
    # 修改订单状态 -- PUT
    url(r"^alipay/$", views.AliPaymentView.as_view()),
]
