from django_redis import get_redis_connection
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, GenericAPIView, CreateAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings

from docs import constants
from goods.serializers import SKUSerializer
from goods.models import SKU
from users import serializer
from users.serializer import UserAddressSerializer, AddressTitleSerializer, AddBrowseHistorySerializer


class UserDetailView(RetrieveAPIView):
    """用户详情 -- 需登陆
    GET /users/detail/
    """

    # 指定序列化器
    serializer_class = serializer.UserDetailSerializer
    # 验证用户 -- 获取登陆用户
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """重写 -- 获取实体类信息"""

        # 返回已登录的用户信息
        user = self.request.user
        # 生成消息体(函数)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成JWT认证(函数)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 根据用户信息生成消息体
        payload = jwt_payload_handler(user)
        # 根据消息体生成JWT认证
        token = jwt_encode_handler(payload)
        # 生成的jwt 序列化返回
        user.token = token
        # 返回用户信息
        return user


class EmailView(UpdateAPIView):
    """修改用户邮箱（修改用户的邮箱字段）
    PUT /users/email/
    """

    # 指定序列化器
    serializer_class = serializer.EmailSerializer
    # 获取登陆用户
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """重写 -- 获取实体类信息"""

        # 自定义返回当前登陆用户
        return self.request.user


class AddressCount(GenericAPIView):
    """获取当前用户收货地址总数
    GET /users/address/count/
    """
    # 获取登陆用户
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """GET请求 -- 获取当前用户收货地址"""

        # 获取当前登陆用户地址总数
        count = request.user.addresses.filter(is_deleted=False).count()
        # 此视图只应返回当前用户的收货地址数量, 不应该做判断
        # if count >= 10:
        #     return Response({'message': '收货地址个数已达到上限, 无法新增收货地址'}, status=400)
        # 返回当前用户收货地址数量
        return Response({"count": count})


class AddressViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """用户地址管理视图集
    POST    /addresses/             新建  -> create
    PUT     /addresses/<pk>/        修改  -> update
    GET     /addresses/             查询  -> list
    DELETE  /addresses/<pk>/        删除  -> destroy
    PUT     /addresses/<pk>/status/ 设置默认    -> status
    PUT     /addresses/<pk>/title/  设置标题    -> title
    """

    # 序列化器
    serializer_class = UserAddressSerializer
    # 验证身份
    permission_classes = [IsAuthenticated]

    # 查询集 -- 所有数据
    # query_set = Address.objects.all()

    def get_queryset(self):
        """获取查询集合
        自定义 -- 获取当前登录用户未删除的地址
        """

        # 返回当前登陆用户为删除的地址
        # return Address.objects.filter(user=self.request.user, is_deleted=False)
        return self.request.user.addresses.filter(is_deleted=False)
        # return Address.objects.all()

    def list(self, request, *args, **kwargs):
        """用户地址列表数据"""

        # 获取查询集合 -- 当前登陆用户未删除的地址
        queryset = self.get_queryset()
        # 获取序列化器, many=True多数据
        serializer = self.get_serializer(queryset, many=True)
        # 获取当前登陆用户
        user = self.request.user
        # 返回数据
        return Response({
            # 用户ID
            'user_id': user.id,
            # 默认收货地址ID
            'default_address_id': user.default_address_id,
            # 收货地址数量上限
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            # 用户地址列表信息 -- 序列化
            'addresses': serializer.data,
        })

    def create(self, request, *args, **kwargs):
        """重写 -- 用户地址保存"""

        # 获取当前用户收货地址总数
        count = self.request.user.addresses.filter(is_deleted=False).count()
        # 如果当前用户收货地址总数 大于等于 10
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            # 返回异常信息
            return Response({"message": "保存地址数据已达到上限"}, status=400)
        # 调用父类创建数据
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """用户地址删除"""

        # 获取当前登陆用户收货地址
        # address_ = Address.objects.filter(user=self.request.user, pk=kwargs.get("pk"))[0]
        address_ = self.get_object()
        # 设置逻辑删除
        address_.is_deleted = True
        # 保存收货地址
        address_.save()
        # 返回删除成功
        return Response({"message": "ok"}, status=204)

    # 请求方式PUT, 路径和请求资源一致[如: PUT xxx/<pk>/函数名]
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """修改默认地址"""

        # 获取当前用户pk=pk地址
        address = self.get_object()
        # 设置当前登陆用户默认收货地址为当前pk地址
        request.user.default_address = address
        # 用户信息保存
        request.user.save()
        # 返回修改成功
        return Response({'message': 'OK'}, )

    # 请求方式PUT, 路径和请求资源一致[如: PUT xxx/<pk>/函数名]
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """修改标题"""

        # 获取当前用户pk=pk地址
        address = self.get_object()
        # 实例化序列化器
        serializer = AddressTitleSerializer(instance=address, data=request.data)
        # 校验
        serializer.is_valid(raise_exception=True)
        # 保存数据
        serializer.save()
        # 返回
        return Response(serializer.data)


class BrowseHistoryView(CreateAPIView):
    """用户浏览记录"""

    # 校验登陆用户
    permission_classes = [IsAuthenticated]
    # 设置序列化器
    serializer_class = AddBrowseHistorySerializer

    def get(self, request):
        """查询用户浏览记录"""

        # 获取user_id
        user_id = request.user.id
        # 获取可以操作redis服务器的对象
        redis_conn = get_redis_connection('history')
        # 查询出redis中用户存储的浏览记录
        sku_ids = redis_conn.lrange('history_%s' % user_id, 0, -1)
        # 查询sku列表数据
        sku_list = []
        for sku_id in sku_ids:
            # 获取sku信息
            sku = SKU.objects.get(id=sku_id)
            # 添加到列表
            sku_list.append(sku)

        # 调用序列化器实现输出：序列化器序列化操作
        serializer = SKUSerializer(sku_list, many=True)
        # 返回
        return Response(serializer.data)
