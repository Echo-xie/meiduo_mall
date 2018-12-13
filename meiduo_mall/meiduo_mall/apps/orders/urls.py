"""订单子应用路由

date: 18-12-11 下午2:40
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # 确认订单
    url(r'^settlement/$', views.OrderSettlementView.as_view()),
    # 订单操作
    url(r"^action/$", views.OrderAPIView.as_view())
]
