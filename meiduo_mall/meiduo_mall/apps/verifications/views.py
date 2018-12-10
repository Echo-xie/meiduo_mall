from django.conf import settings
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer, BadData
from redis import StrictRedis
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from carts.utils import merge_cart_cookie_to_redis
from meiduo_mall.utils.exceptions import logger
from celery_tasks.sms.tasks import *
from users.models import User
from users.serializer import UserRegisterSerializer, UserSerializerBase, UserPassWordSerializer


class SMSCodeView(APIView):
    """发送短信验证码类视图"""

    def get(self, request, mobile):
        """get请求
        GET /vm/sms_code/(?P<mobile>1[3-9]\d{9})/

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
    serializer_class = UserSerializerBase

    def check_username(self, request, username):
        """判断用户名是否存在
        GET /vm/username/(?P<username>\w{5,20})/count/

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
        GET /vm/mobile/(?P<mobile>1[3-9]\d{9})/count/

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
    GET /vm/user_register/
    """
    # 指定序列化器
    serializer_class = UserRegisterSerializer


class VerifyEmailView(APIView):
    """激活用户邮箱"""

    def get(self, request):
        # 获取token
        token = request.query_params.get('token')
        # 如果没有token
        if not token:
            return Response({'message': '缺少token'}, status=400)

        # 验证token -- 10分钟
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=10 * 60)
        try:
            # 解密
            data = serializer.loads(token)
        except BadData:
            # 解密异常 -- 抛出异常
            return Response({'message': '链接信息无效'}, status=400)

        # 获取解密后的邮箱
        email = data.get('email')
        # 获取解密后的用户ID
        user_id = data.get('user_id')
        try:
            # 根据用户ID和邮箱获取用户信息
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            # 抛出异常
            return Response({'message': '激活用户不存在'}, status=400)

        # 修改用户邮箱激活状态
        user.email_active = True
        # 保存记录
        user.save()

        return Response({'message': 'OK'})


class PassWordViewSet(UpdateModelMixin, GenericViewSet):
    """用户密码管理视图集
    GET /vm/password/<pk>/if_right/ -- 验证密码
    PUT /vm/password/<pk>/ -- 修改密码

    """
    # 序列化器
    serializer_class = UserPassWordSerializer
    # 验证身份
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    # GET请求
    @action(methods=["get"], detail=True)
    def if_right(self, request, pk):
        """校验密码"""

        # 校验请求密码和原密码是否一致
        result = self.get_object().check_password(pk)
        # 如果不一致
        if not result:
            # 提示错误信息
            return Response({"message": "密码错误"}, status=400)
        # 密码一致
        return Response({"message": "ok"})


class UserAuthorizeView(ObtainJSONWebToken):
    """重写 -- Django用户认证方法"""

    def post(self, request, *args, **kwargs):
        # 调用父类用户认证方法, 获取返回结果
        response = super().post(request, *args, **kwargs)

        # 实例化序列化器
        serializer = self.get_serializer(data=request.data)
        # 反序列化校验数据
        if serializer.is_valid():
            # serializer: JSONWebTokenSerializer
            # 序列化器校验通过后返回了登录成功的user对象
            user = serializer.validated_data.get('user')
            # 合并购物车商品
            response = merge_cart_cookie_to_redis(request, response, user)
        # 返回响应
        return response
