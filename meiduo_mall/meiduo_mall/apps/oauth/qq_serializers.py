"""QQ登陆序列化器

date: 18-12-5 下午6:36
"""
from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.models import OAuthQQUser
from users.models import User


class QQUserSerializer(serializers.Serializer):
    """ QQ登录创建用户序列化器

    """
    openid = serializers.CharField(label='openid', write_only=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$', write_only=True)
    password = serializers.CharField(label='密码', max_length=20, min_length=8, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)

    def validate(self, attrs):
        """校验

        :param attrs: 反序列化数据
        :return:
        """
        # 手机
        mobile = attrs['mobile']
        # 短信验证码
        sms_code = attrs['sms_code']
        # 密码
        password = attrs['password']

        # 获取Redis数据库连接
        redis_conn = get_redis_connection('sms_codes')
        # 获取短信验证码数据
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        # 如果没有短信验证码数据
        if not real_sms_code:
            # 抛出异常
            raise serializers.ValidationError({'message': '短信验证码无效'})
        # 如果短信验证码和短信验证码数据不一致
        if real_sms_code.decode() != sms_code:
            # 抛出异常
            raise serializers.ValidationError({'message': '短信验证码错误'})

        try:
            # 根据手机号查询美多用户
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 如果用户不存在, 则自动新增一个美多用户, 再进行绑定
            user = User.objects.create_user(
                username=mobile,
                password=password,
                mobile=mobile)
        else:
            # 如果要绑定的用户存在, 则校验密码是否正确
            if not user.check_password(password):
                raise serializers.ValidationError({'message': '密码错误'})

        # 将认证后的user放进校验字典中，绑定关联时用到
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """创建记录

        :param validated_data: 校验后数据
        :return:
        """
        # 获取校验的用户
        user = validated_data.get('user')
        openid = validated_data.get('openid')

        # 绑定openid和美多用户： 新增一条表数据
        OAuthQQUser.objects.create(
            openid=openid,
            user=user
        )
        return user  # 返回美多用户对象
