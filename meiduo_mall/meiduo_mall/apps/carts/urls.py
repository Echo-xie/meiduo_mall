"""

date: 18-12-10 下午3:05
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    # 购物车[增删改查]
    url(r"^action/$", views.CartView.as_view()),
    # 购物车全选/全不选
    url(r'^selection/$', views.CartSelectAllView.as_view()),
]
