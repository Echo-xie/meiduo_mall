from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users import user_serializer
from users.user_serializer import UserAddressSerializer


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


class AddressCount(APIView):

    def get(self, request):
        count = request.user.addresses.count()
        if count >= 10:
            return Response({'message': '收货地址个数已达到上限, 无法新增收货地址'}, status=400)
        return Response({"message": "ok"})


class AddressViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """ 用户地址管理 """
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    # query_set = Address.objects.all()

    def get_queryset(self):
        # 获取当前登录用户的地址
        # return = Address.objects.filter(user=self.request.user, is_deleted=False)
        return self.request.user.addresses.filter(is_deleted=False)
