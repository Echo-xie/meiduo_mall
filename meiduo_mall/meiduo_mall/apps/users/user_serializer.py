"""用户子应用序列化器

date: 18-12-1 下午10:49
"""
from rest_framework.serializers import ModelSerializer
import re

from rest_framework_jwt.settings import api_settings

from meiduo_mall.utils.common import get_sms_code_by_mobile
from users.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UsersSerializerBase(ModelSerializer):
    """实体类 用户序列化器 -- 基类

    """

    class Meta:
        # 指定实体类
        model = User
        # 指定字段
        fields = "__all__"


class UserRegisterSerializer(ModelSerializer):
    """用户注册序列化器

    """
    # write_only: 只写[写入], 只用于反序列化, 不进行序列化
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.BooleanField(label='同意协议', write_only=True)
    # 添加 token字段, 令牌用于jwt认证, read_only: 只读[读取], 只用于序列化, 不进行反序列化
    token = serializers.CharField(label='登录状态token', read_only=True)

    class Meta:
        # 指定实体类
        model = User
        # 字段展示
        fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow', "token")

        # 修改字段规则
        extra_kwargs = {
            # 用户名
            'username': {
                # 最小长度
                'min_length': 5,
                # 最大长度
                'max_length': 20,
                # 错误信息
                'error_messages': {
                    # 最小长度错误
                    'min_length': '仅允许5-20个字符的用户名',
                    # 最大长度错误
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            # 密码
            'password': {
                # 只写
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    """自定义校验规则"""

    def validate(self, attrs):
        # 获取请求体数据
        # 密码
        _password = attrs['password']
        # 确认密码
        _password2 = attrs['password2']
        # 手机号码
        _mobile = attrs['mobile']
        # 短信验证码
        _sms_code = attrs['sms_code']
        # 同意协议
        _allow = attrs["allow"]

        # 如果两次密码不一致
        if _password != _password2:
            # 抛出异常
            raise ValidationError('两次密码不一致')
        # 如果手机号码不匹配
        if not re.match(r'^1[3-9]\d{9}$', _mobile):
            # 抛出异常
            raise ValidationError('手机号格式错误')
        # 调用通用工具获取手机短信验证码
        real_sms_code = get_sms_code_by_mobile(mobile=_mobile)
        # 如果数据库没有此手机号码数据
        if real_sms_code is None:
            # 抛出异常
            raise ValidationError('无效的短信验证码')
        # 如果用户输入短信验证码和数据库的数据不一致
        if _sms_code != real_sms_code:
            # 抛出异常
            raise ValidationError('短信验证码错误')

        # 如果没有同意协议
        if not _allow:
            # 抛出异常
            raise ValidationError('请同意用户协议')
        # 返回表单数据
        return attrs

    def create(self, validated_data):
        """重写创建函数 -- 指定保存字段

        :param validated_data: 验证后数据
        :return:
        """
        # 不会对密码进行加密
        # User.objects.create()
        # 会对密码进行加密 -- 自定义保存属性
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            mobile=validated_data.get('mobile'))
        # 注册成功添加数据后, 生成JWT返回客户端自动登陆
        # 导包： from rest_framework_jwt.settings import api_settings
        # 生成消息体(函数)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成JWT认证(函数)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # {'user_id': x, 'email': '', 'username': '136xxxxxxxx', 'exp': 1539048426}
        # 根据用户信息生成消息体
        payload = jwt_payload_handler(user)
        # 根据消息体生成JWT认证
        token = jwt_encode_handler(payload)
        # 生成的jwt 序列化返回
        user.token = token
        return user
