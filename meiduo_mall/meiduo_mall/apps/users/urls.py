from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # 个人中心 -- 用户详情
    url(r'^detail/$', views.UserDetailView.as_view()),
    # 保存邮箱
    url(r'^email/$', views.EmailView.as_view()),
    # 获取收货地址数量
    url(r'^address/count/$', views.AddressCount.as_view()),
]

router = DefaultRouter()
# 用户收货地址, 增删改查视图集 -- 视图集不用正则表达开头和结尾, 自带
router.register(r'addresses', views.AddressViewSet, base_name='addresses')
urlpatterns += router.urls
