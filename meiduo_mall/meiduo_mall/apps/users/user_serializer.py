"""用户子应用序列化器

date: 18-12-1 下午10:49
"""
from rest_framework.serializers import ModelSerializer
import re
from rest_framework_jwt.settings import api_settings
from celery_tasks.email.tasks import send_verify_email
from meiduo_mall.utils.common import get_sms_code_by_mobile
from users.models import User, Address
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.utils import generate_verify_email_url


class UserSerializerBase(ModelSerializer):
    """实体类 用户序列化器 -- 基类"""

    class Meta:
        """元数据"""
        # 指定实体类
        model = User
        # 指定字段
        fields = "__all__"


class UserDetailSerializer(UserSerializerBase):
    """ 用户详细信息序列化器"""
    # 添加 token字段, 令牌用于jwt认证, read_only: 只读[读取], 只用于序列化, 不进行反序列化
    token = serializers.CharField(label='登录状态token', read_only=True)

    class Meta:
        """元数据"""
        # 指定实体类
        model = User
        # 指定字段
        fields = ('id', 'username', 'mobile', 'email', 'email_active', "token")


class UserRegisterSerializer(ModelSerializer):
    """用户注册序列化器"""
    # write_only: 只写[写入], 只用于反序列化, 不进行序列化
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.BooleanField(label='同意协议', write_only=True)
    # 添加 token字段, 令牌用于jwt认证, read_only: 只读[读取], 只用于序列化, 不进行反序列化
    token = serializers.CharField(label='登录状态token', read_only=True)

    class Meta:
        """元数据"""
        # 指定实体类
        model = User
        # 字段
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


class EmailSerializer(serializers.ModelSerializer):
    """修改用户邮箱序列化器"""

    class Meta:
        """元数据"""
        # 实体类
        model = User
        # 字段
        fields = ('id', 'email')
        # 自定义字段规则
        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        """更新记录 -- 重写

        :param instance:
        :param validated_data:
        :return:
        """
        # 获取邮箱
        email = validated_data['email']
        # 赋值
        instance.email = email
        # 保存信息
        instance.save()

        # 获取激活邮箱url
        verify_url = generate_verify_email_url(instance.id)
        # 发送邮箱 -- celery
        send_verify_email.delay(email, verify_url)

        return instance


class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址序列化器
    """
    # 将ID转为字符串展示在页面
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)

    # 后台新增地址时直接输入ID即可
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)

    class Meta:
        """元数据"""
        # 指定实体类
        model = Address
        # 排除字段
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def validate(self, attrs):
        mobile = attrs["mobile"]
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号格式错误')
        return attrs

    # def validate_mobile(self, value):
    #     if not re.match(r'^1[3-9]\d{9}$', value):
    #         raise serializers.ValidationError('手机号格式错误')
    #     return super().validated_data()

    def create(self, validated_data):
        """保存"""
        # self.context['request'].user ：获取当前登录用户对象
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AddressTitleSerializer(serializers.ModelSerializer):
    """地址标题序列化器"""

    class Meta:
        """元数据"""
        # 实体类
        model = Address
        # 字段
        fields = ('title',)


class UserPassWordSerializer(serializers.ModelSerializer):
    """修改密码序列化器"""

    # 旧密码
    old_password = serializers.CharField(write_only=True)
    # 新密码
    new_password = serializers.CharField(write_only=True)
    # 确认密码
    new_password2 = serializers.CharField(write_only=True)

    class Meta:
        """元数据"""
        # 实体类
        model = User
        # 字段
        fields = ("old_password", "new_password", "new_password2")

    def validate(self, attrs):
        """自定义校验"""

        # 获取属性
        old_password = attrs["old_password"]
        new_password = attrs["new_password"]
        new_password2 = attrs["new_password2"]
        # 获取当前登陆用户
        user_ = self.context['request'].user

        # 如果旧密码校验失败
        if not user_.check_password(old_password):
            #
            raise ValidationError("当前密码错误")

        # 如果两次密码不一致
        if new_password != new_password2:
            #
            raise ValidationError("两次密码不一致")

        # 返回校验后的属性
        return attrs

    def update(self, instance, validated_data):
        """更新"""

        # 设置新密码
        instance.set_password(validated_data["new_password"])
        # 保存数据
        instance.save()
        # 返回更新后数据
        return instance
