from django.conf.urls import url
from . import views

urlpatterns = [
    # 首页
    url(r'^index/$', views.index),
    # 模块测试
    url(r'^templates_test/$', views.templates_test),
    # 跨域请求测试
    url(r'^cross_domain_test/$', views.cross_domain_test.as_view()),
]
