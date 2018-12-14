"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # admin站点
    url(r'^admin/', admin.site.urls),
    # CKEditor富文本路由
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # 用户子应用
    url(r'^users/', include("users.urls")),
    # 校验子应用
    url(r"^vm/", include("verifications.urls")),
    # 第三方开放平台
    url(r"^oauth/", include("oauth.urls")),
    # 省市区管理
    url(r"^areas/", include("areas.urls")),
    # 商品
    url(r"^goods/", include("goods.urls")),
    # 广告
    url(r"^contents/", include("contents.urls")),
    # 购物车
    url(r"^carts/", include("carts.urls")),
    # 订单
    url(r"^orders/", include("orders.urls")),
    # 订单支付
    url(r"^payment/", include("orders.urls")),
]
