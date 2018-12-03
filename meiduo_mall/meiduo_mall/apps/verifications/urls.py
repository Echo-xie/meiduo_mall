"""验证子应用路由配置

date: 18-12-1 下午9:43
"""
from django.conf.urls import url
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
    url(r"authorizations/$", obtain_jwt_token)

]
