from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer, BadData
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users import user_serializer
from users.models import User


class UserDetailView(RetrieveAPIView):
    """用户详情

    """
    # 指定序列化器
    serializer_class = user_serializer.UsersSerializerBase
    # 获取登陆用户
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """重写 -- 获取实体类信息

        :return:
        """
        # 返回已登录的用户信息
        return self.request.user


class EmailView(UpdateAPIView):
    """修改用户邮箱（修改用户的邮箱字段）

    """
    # 指定序列化器
    serializer_class = user_serializer.EmailSerializer
    # 获取登陆用户
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """重写 -- 获取实体类信息

        :return:
        """
        # 自定义返回当前登陆用户
        return self.request.user
