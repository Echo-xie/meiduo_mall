from django.conf.urls import url
from . import views

urlpatterns = [
    # 面包屑导航
    url(r"^categories/(?P<pk>\d+)/$", views.CategoryView.as_view()),
    # 类别列表
    url(r'^skus/$', views.SKUListView.as_view()),
]
