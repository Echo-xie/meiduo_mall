"""

date: 18-12-5 下午3:19
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    # 获取QQ登陆url
    url(r"^qq/authorization/$", views.QQURLView.as_view()),
    # QQ用户登陆后回调处理
    url(r'^qq/user/$', views.QQUserView.as_view()),
]

