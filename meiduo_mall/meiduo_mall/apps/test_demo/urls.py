"""子应用路由信息

"""
from django.conf.urls import url

from . import views

# 路由列表
urlpatterns = [
    # 配置路由 -- 通过url函数(路径, 视图[, 路由名称])
    # [函数视图]
    url(r"^index/$", views.index, name="demo_index"),  # 首页
    url(r"^index/(?P<pk>\d+)/$", views.index_pk, name="demo_index_pk"),  # 首页带路径参数
    url(r"^index_query/$", views.index_query, name="demo_index_query"),  # 首页带查询参数
    url(r"^index_post/$", views.index_post, name="demo_index_post"),  # 首页带表单参数
    url(r"^index_json/$", views.index_json, name="demo_index_json"),  # 首页带json参数
    url(r"^reverse_index/$", views.reverse_index),  # 重定向反编译url -- 首页
    url(r"^reverse_index_pk/(?P<pk>\d+)/$", views.reverse_index_pk),  # 重定向反编译url -- 首页路径参数
    url(r"^reverse_index_query/$", views.reverse_index_query),  # 重定向反编译url -- 首页带查询参数
    # [类视图]
    url(r"^register/$", views.RegisterView.as_view(), name="register"),  # 注册类视图
    # [模板视图]
    url(r"^template_index/$", views.template_index, name="template_index")  # 模板首页
]
