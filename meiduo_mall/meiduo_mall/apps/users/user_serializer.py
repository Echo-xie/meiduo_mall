"""用户子应用序列化器

date: 18-12-1 下午10:49
"""
from rest_framework.serializers import ModelSerializer
import re
from django_redis import get_redis_connection
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
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.BooleanField(label='同意协议', write_only=True)

    def create(self, validated_data):
        # User.objects.create()             # 不会对密码进行加密
        return User.objects.create_user(  # 会对密码进行加密
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            mobile=validated_data.get('mobile'))

    class Meta:
        # 指定实体类
        model = User
        # 字段展示
        fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow')
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

    def validate_mobile(self, value):
        """验证手机号

        :param value: 手机号码
        :return: 手机号码
        """
        # 如果手机号码不匹配
        if not re.match(r'^1[3-9]\d{9}$', value):
            # 抛出异常
            raise ValidationError('手机号格式错误')
        # 返回手机号码
        return value

    def validate_allow(self, value):
        """检验用户是否同意协议

        :param value: 是否同意协议
        :return: 是否同意协议
        """
        # 如果没有同意协议
        if not value:
            # 抛出异常
            raise ValidationError('请同意用户协议')
        # 返回是否同意协议
        return value

    def validate(self, attrs):
        # 如果两次密码不一致
        if attrs['password'] != attrs['password2']:
            # 抛出异常
            raise ValidationError('两次密码不一致')

        # 访问配置信息, 获取数据库连接
        redis_conn = get_redis_connection('sms_codes')
        # 获取表单数据 -- 手机号码
        mobile = attrs['mobile']
        # 获取此手机号码在数据库中的数据
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        # 如果数据库没有此手机号码数据
        if real_sms_code is None:
            # 抛出异常
            raise ValidationError('无效的短信验证码')
        # 如果用户输入短信验证码和数据库的数据不一致
        if attrs['sms_code'] != real_sms_code.decode():
            # 抛出异常
            raise ValidationError('短信验证码错误')
        # 返回表单数据
        return attrs
