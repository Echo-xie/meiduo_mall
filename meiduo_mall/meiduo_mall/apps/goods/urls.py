from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # 面包屑导航
    url(r"^categories/(?P<pk>\d+)/$", views.CategoryView.as_view()),
    # 商品列表
    url(r'^skus_list/$', views.SKUListView.as_view()),
]

router = DefaultRouter()
# 商品查询
router.register('skus_search', views.SKUSearchViewSet, base_name='skus_search')
urlpatterns += router.urls
