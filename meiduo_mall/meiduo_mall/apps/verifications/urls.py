"""验证子应用路由配置

date: 18-12-1 下午9:43
"""
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # 发送短信验证码
    url(r'^sms_code/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
    # 校验用户名是否重复
    url(r'^username/(?P<username>\w{5,20})/count/$', views.CheckUsersAttr.as_view({'get': 'check_username'})),
    # 校验手机号码是否重复
    url(r'^mobile/(?P<mobile>1[3-9]\d{9})/count/$', views.CheckUsersAttr.as_view({'get': 'check_mobile'})),
    # 用户注册
    url(r'^user_register/$', views.UserRegister.as_view()),
    # 用户登陆 -- 调用JWT的验证登陆
    # url(r"^authorizations/$", obtain_jwt_token),
    # 用户登陆 -- 重写JWT的验证登陆, 添加购物车合并
    url(r"^authorizations/$", views.UserAuthorizeView.as_view()),
    # 用户激活邮箱验证
    url(r"^email/$", views.VerifyEmailView.as_view()),
    # 用户密码校验
    # url(r'^check_password/(?P<password>\w+)/$', views.PassWordViewSet.as_view({'get': 'check_password'})),
    # 修改用户密码
    # url(r'^password/$', views.PassWordViewSet.as_view({"put": "update"})),
]

router = DefaultRouter()
# 用户收货地址, 增删改查视图集 -- 视图集不用正则表达开头和结尾, 自带
router.register(r'password', views.PassWordViewSet, base_name='password')
urlpatterns += router.urls
