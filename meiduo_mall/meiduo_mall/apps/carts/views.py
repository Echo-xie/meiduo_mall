from rest_framework.views import APIView
from carts.serializers import CartSerializer, CartDeleteSerializer, CartSelectAllSerializer
from carts.utils import CartsData


class CartView(APIView):
    """购物车视图 -- 未登陆用户购物车存放在cookie中
    GET carts/action/
    POST carts/action/
    PUT carts/action/
    DELETE carts/action/

    """

    def perform_authentication(self, request):
        """重写 -- 执行身份证认证
        drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
        如果认证不通过,则会抛异常返回401状态码
        问题: 抛异常会导致视图无法执行
        解决: 捕获异常即可
        """
        try:
            super().perform_authentication(request)
        except Exception as e:
            print("购物车子应用, 可不用登陆 -- ", e)

    def get(self, request):
        """查询购物车所有的商品"""

        return CartsData(action="GET", request=request, serializer_class=None).run()

    def post(self, request):
        """添加购物车"""

        return CartsData(action="POST", request=request, serializer_class=CartSerializer).run()

    def put(self, request):
        """修改购物车数据"""

        return CartsData(action="PUT", request=request, serializer_class=CartSerializer).run()

    def delete(self, request):
        """删除购物车数据"""

        return CartsData(action="DELETE", request=request, serializer_class=CartDeleteSerializer).run()


class CartSelectAllView(APIView):
    """购物车全选和全不选
    PUT carts/selection/
    """

    def perform_authentication(self, request):
        """重写 -- 执行身份证认证
        drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
        如果认证不通过,则会抛异常返回401状态码
        问题: 抛异常会导致视图无法执行
        解决: 捕获异常即可
        """
        try:
            super().perform_authentication(request)
        except Exception as e:
            print("购物车子应用, 可不用登陆 -- ", e)

    def put(self, request):
        """修改购物车商品信息 -- 全选或全不选"""

        return CartsData(action="SELECTION", request=request, serializer_class=CartSelectAllSerializer).run()

# 未封装前
# class CartView(APIView):
#     """购物车视图 -- 未登陆用户购物车存放在cookie中
#     GET carts/action/
#     POST carts/action/
#     PUT carts/action/
#     DELETE carts/action/
#
#     """
#
#     def perform_authentication(self, request):
#         """重写 -- 执行身份证认证
#         drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
#         如果认证不通过,则会抛异常返回401状态码
#         问题: 抛异常会导致视图无法执行
#         解决: 捕获异常即可
#         """
#         try:
#             super().perform_authentication(request)
#         except Exception as e:
#             print("购物车子应用, 可不用登陆 -- ", e)
#
#     def get(self, request):
#         """查询购物车所有的商品"""
#
#         user = request.user
#         # 用户已登录，从redis中读取
#         if user.is_authenticated():
#             redis_conn = get_redis_connection('carts')
#             pl = redis_conn.pipeline
#             dict_cart = pl.hgetall('cart_%s' % user.id)  # {1: 2, 2: 2}
#             list_cart_selected = pl.smembers('cart_selected_%s' % user.id)
#             pl.execute()
#
#             # 拼装字典
#             # {1:{'count':2, 'selected':False}, 2:{'count':2, 'selected':False}}
#             cart = {}
#             for sku_id, count in dict_cart.items():
#                 cart[int(sku_id)] = {
#                     'count': int(count),
#                     'selected': sku_id in list_cart_selected
#                 }
#         else:
#             # 用户未登录，从cookie中读取
#             cart = request.COOKIES.get('cart')
#             if cart is not None:
#                 # 购物车base64字符串 --> 字典
#                 cart = pickle.loads(base64.b64decode(cart.encode()))
#                 # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
#                 print('cookie: ', cart)
#             else:
#                 cart = {}
#
#         # 查询购物车中所有的商品
#         skus = SKU.objects.filter(id__in=cart.keys())
#         # 给sku对象新增两个字段: 商品数量和勾选状态
#         for sku in skus:
#             sku.count = cart[sku.id]['count']
#             sku.selected = cart[sku.id]['selected']
#
#         # 响应序列化数据
#         serializer = CartSKUSerializer(skus, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         """添加购物车"""
#
#         # 创建序列化器，校验请求参数是否合法
#         serializer = CartSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         # 获取请求参数
#         sku_id = serializer.validated_data.get('sku_id')
#         count = serializer.validated_data.get('count')
#         selected = serializer.validated_data.get('selected')
#
#         user = request.user
#         if user.is_authenticated():  # 判断是否已登录
#             # 用户已登录，在redis中保存
#             redis_conn = get_redis_connection('carts')
#             pl = redis_conn.pipeline()
#             # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
#             # 增加购物车商品数量
#             pl.hincrby('cart_%s' % user.id, sku_id, count)
#             # 保存商品勾选状态
#             if selected:
#                 pl.sadd('cart_selected_%s' % user.id, sku_id)
#             pl.execute()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             # 1. 从cookie中获取购物车信息
#             cart = request.COOKIES.get('cart')
#
#             # 2. base64字符串 -> 字典
#             if cart is not None:
#                 cart = pickle.loads(base64.b64decode(cart.encode()))
#             else:
#                 cart = {}
#         # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
#
#         print('cookies: ', cart)
#
#         # 3. 新增字典中对应的商品数量
#         sku = cart.get(sku_id)
#         if sku:  # 原有数量 + 新增数量
#             count += int(sku.get('count'))
#
#         cart[sku_id] = {
#             'count': count,
#             'selected': selected
#         }
#
#         # 4. 字典 --> base64字符串
#         cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
#
#         # 5. 通过cookie保存购物车数据（base64字符串）
#         response = Response(serializer.data, status=201)
#         # 参数3：cookie有效期
#         response.set_cookie('cart', cookie_cart, constants.CART_COOKIE_EXPIRES)
#         return response
#
#     def put(self, request):
#         """
#         修改购物车数据
#         """
#         # 校验参数
#         serializer = CartSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # 获取校验后的参数
#         sku_id = serializer.validated_data.get('sku_id')
#         count = serializer.validated_data.get('count')
#         selected = serializer.validated_data.get('selected')
#
#         user = request.user
#         if user.is_authenticated():
#             # 用户已登录，在redis中保存
#             redis_conn = get_redis_connection('carts')
#             pl = redis_conn.pipeline()
#             # 修改商品数量
#             pl.hset('cart_%s' % user.id, sku_id, count)
#             # 修改商品的勾选状态
#             if selected:
#                 pl.sadd('cart_selected_%s' % user.id, sku_id)
#             else:
#                 pl.srem('cart_selected_%s' % user.id, sku_id)
#             pl.execute()
#             return Response(serializer.data)
#         else:
#             # 1. 从cookie中获取购物车信息
#             cart = request.COOKIES.get('cart')
#             # 2. base64字符串 -> 字典
#             if cart is not None:
#                 cart = pickle.loads(base64.b64decode(cart.encode()))
#             else:
#                 cart = {}
#             # 3. 修改字典中对应的商品数量和选中状态
#             cart[sku_id] = {
#                 'count': count,
#                 'selected': selected
#             }
#             # 4. 字典 --> base64字符串
#             cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
#             # 5. 通过cookie保存购物车数据（base64字符串）
#             response = Response(serializer.data)
#             response.set_cookie('cart', cookie_cart, constants.CART_COOKIE_EXPIRES)
#             return response
#
#     def delete(self, request):
#         """
#         删除购物车数据
#         """
#         serializer = CartDeleteSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         sku_id = request.data['sku_id']
#
#         user = request.user
#         if user.is_authenticated():
#             # 用户已登录，在redis中保存
#             redis_conn = get_redis_connection('carts')
#             pl = redis_conn.pipeline()
#             pl.hdel('cart_%s' % user.id, sku_id)
#             pl.srem('cart_selected_%s' % user.id, sku_id)
#             pl.execute()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             # 用户未登录，在cookie中保存
#             response = Response(status=status.HTTP_204_NO_CONTENT)
#             # 1. 从cookie中获取购物车信息
#             cart = request.COOKIES.get('cart')
#             if cart is not None:
#                 # 2. base64字符串 -> 字典
#                 cart = pickle.loads(base64.b64decode(cart.encode()))
#                 # 3. 如果商品在字典中，删除字典中对应的商品
#                 if sku_id in cart:
#                     del cart[sku_id]
#                     # 4. 字典 --> base64字符串
#                     cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
#                     # 5. 通过cookie保存购物车数据（base64字符串）
#                     response.set_cookie('cart', cookie_cart,
#                                         constants.CART_COOKIE_EXPIRES)
#             return response
#
#
# class CartSelectAllView(APIView):
#     """购物车全选和全不选
#     PUT carts/selection/
#     """
#
#     def perform_authentication(self, request):
#         """重写 -- 执行身份证认证
#         drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
#         如果认证不通过,则会抛异常返回401状态码
#         问题: 抛异常会导致视图无法执行
#         解决: 捕获异常即可
#         """
#         try:
#             super().perform_authentication(request)
#         except Exception as e:
#             print("购物车子应用, 可不用登陆 -- ", e)
#
#     def put(self, request):
#         """修改购物车商品信息 -- 全选或全不选"""
#
#         # 实例化序列化器
#         serializer = CartSelectAllSerializer(data=request.data)
#         # 反序列化校验
#         serializer.is_valid(raise_exception=True)
#         # 获取校验成功后数据
#         selected = serializer.validated_data['selected']
#         # 获取当前用户
#         user = request.user
#         # 如果已登录 -- 数据在Redis中保存
#         if user.is_authenticated():
#             # 获取数据库连接
#             redis_conn = get_redis_connection('carts')
#             # 查询数据库获取数据
#             sku_id_list = redis_conn.hkeys('cart_%s' % user.id)
#             # 如果是全选
#             if selected:
#                 # 添加购物车商品勾选信息, 拆包sku_id_list
#                 redis_conn.sadd('cart_selected_%s' % user.id, *sku_id_list)
#             # 否则
#             else:
#                 # 删除购物车商品勾选信息, 拆包sku_id_list
#                 redis_conn.srem('cart_selected_%s' % user.id, *sku_id_list)
#             # 返回响应
#             return Response({'message': 'OK'})
#         # 未登陆 -- 数据在cookie中
#         else:
#             # 实例化响应
#             response = Response({'message': 'OK'})
#             # 从cookie中获取购物车信息
#             cart = request.COOKIES.get('cart')
#             # 如果有购物车信息
#             if cart:
#                 # base64字符串 -> 字典
#                 cart = pickle.loads(base64.b64decode(cart.encode()))
#                 # 循环购物车信息
#                 for sku_id in cart:
#                     # 修改所有商品为选中状态
#                     cart[sku_id]['selected'] = selected
#                 # 字典 --> base64字符串
#                 cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
#                 # 设置cookie返回数据, 参数3 = cookie有效期
#                 response.set_cookie('cart', cookie_cart, constants.CART_COOKIE_EXPIRES)
#             # 返回响应
#             return response
