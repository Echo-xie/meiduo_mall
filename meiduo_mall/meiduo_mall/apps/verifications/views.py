from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from meiduo_mall.utils.exceptions import logger
from celery_tasks.sms.tasks import *
from users.models import User
from users.user_serializer import UserRegisterSerializer, UsersSerializerBase


class SMSCodeView(APIView):
    """发送短信验证码类视图

    """

    def get(self, request, mobile):
        """get请求
        url[GET]: /vm/sms_code/(?P<mobile>1[3-9]\d{9})/

        :param request: 请求报文
        :param mobile: 手机
        :return: 响应报文
        """
        # 获取Redis配置中"sms_codes"数据库连接
        strict_redis = get_redis_connection('sms_codes')  # type: StrictRedis
        # Redis管道 -- 批量执行指令
        pipeline_ = strict_redis.pipeline()

        # 获取数据库中此手机号码的数据 -- 用于判断是否频繁获取短信验证码
        send_flag = strict_redis.get('send_flag_%s' % mobile)
        # 如果数据库中有数据
        if send_flag:
            # 抛出校验异常, 频繁获取短信验证码
            # return Response({'message': '发送短信过于频繁'}, status=400)
            raise ValidationError({'message': '发送短信过于频繁'})

        # 生成短信验证码
        import random
        # 生成随机短信验证码, 至少6位数字, 不够补0,
        sms_code = '%06d' % random.randint(0, 999999)
        # 写日志
        logger.info('sms_code: %s' % sms_code)

        # 使用云通讯发送短信验证码获取 -- 耗时操作, 函数执行会阻塞
        # CCP().send_template_sms(mobile, [sms, 5], 1)

        # 调用celery调度任务执行 -- 任务调度, 不会阻塞
        send_sms_code.delay(mobile, sms_code)

        # 设置短信验证码时效, 保存至Redis中
        # strict_redis.setex('sms_%s' % mobile, 5 * 60, sms_code)  # 5分钟
        pipeline_.setex('sms_%s' % mobile, 5 * 60, sms_code)  # 5分钟

        # 设置请求短信验证码时效, 保存至Redis中
        # strict_redis.setex('send_flag_%s' % mobile, 60, 1)  # 1分钟过期
        pipeline_.setex('send_flag_%s' % mobile, 60, 1)  # 1分钟过期

        # 管道执行
        pipeline_.execute()

        # 返回响应
        return Response({'message': 'ok'})


class CheckUsersAttr(GenericViewSet):
    """
        视图集 -- 校验用户属性
    """
    # 查询集
    queryset = User.objects.all()
    # 序列化器
    serializer_class = UsersSerializerBase

    def check_username(self, request, username):
        """判断用户名是否存在
        url[GET]: /vm/username/(?P<username>\w{5,20})/count/

        :param request: 请求报文
        :param username: 用户名
        :return: 响应
        """
        # 查询是否有此用户名的数据总数
        count = User.objects.filter(username=username).count()
        # 封装返回数据
        return_data = {
            # 用户名
            'username': username,
            # 数据总数
            'count': count
        }
        # 返回
        return Response(return_data)

    def check_mobile(self, request, mobile):
        """判断手机号码是否存在
        url[GET]: /vm/mobile/(?P<mobile>1[3-9]\d{9})/count/

        :param request: 请求报文
        :param mobile: 手机号码
        :return: 响应
        """
        # 查询是否有此手机号码的数据总数
        count = User.objects.filter(mobile=mobile).count()
        # 封装返回数据
        return_data = {
            # 手机号码
            'mobile': mobile,
            # 数据总数
            'count': count
        }
        # 返回
        return Response(return_data)


class UserRegister(CreateAPIView):
    """用户注册
    url[GET]: /vm/user_register/
    """
    # 指定序列化器
    serializer_class = UserRegisterSerializer
