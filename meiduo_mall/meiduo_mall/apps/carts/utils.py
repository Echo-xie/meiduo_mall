"""购物车子应用工具

date: 18-12-10 下午7:47
"""
import base64
import pickle

from django_redis import get_redis_connection
from redis.client import StrictPipeline
from rest_framework import status
from rest_framework.response import Response

from carts.serializers import CartSKUSerializer
from docs import constants
from goods.models import SKU


class CartsData(object):
    """操作购物车数据
    根据Request请求报文, 获取对应的购物车数据,
    已登录从Redis中获取购物车数据,
    未登陆从Cookies中获取购物车数据,
    针对不同的action操作购物车数据后封装数据并返回,

    :param action: 动作[GET, POST, PUT, DELETE]
    :param request: 请求报文
    :param serializer_class: 序列化器类
    :return: 响应报文
    """

    def __init__(self, action, request, serializer_class=None):
        """初始化"""

        # 动作
        self.action = action
        # 获取当前用户
        self.user_ = request.user

        # 购物车信息 -- 字典类型
        self.cart = {}
        # cookie购物车信息
        self.cookie_cart = request.COOKIES.get('cart', {})
        # 如果cookie中有购物车信息
        if self.cookie_cart:
            # base64字符串 -> 字典
            # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
            self.cookie_cart = pickle.loads(base64.b64decode(self.cookie_cart.encode()))

        # 获取数据库连接
        redis_conn = get_redis_connection('cart')
        # 生成管道
        self.pl = redis_conn.pipeline()  # type: StrictPipeline

        # 初始化序列化器
        self.serializer = None

        # 初始化请求参数
        # sku_id = None
        # count = None
        # selected = None

        # 判断是否有序列化器类
        if serializer_class:
            # 创建序列化器
            self.serializer = serializer_class(data=request.data)
            # 校验请求参数是否合法
            self.serializer.is_valid(raise_exception=True)

            # 获取请求参数
            self.sku_id = self.serializer.validated_data.get('sku_id')
            self.count = self.serializer.validated_data.get('count')
            self.selected = self.serializer.validated_data.get('selected')

    def get_action(self):
        """获取购物车数据"""

        # 如果是已登录用户 -- 数据存储在Redis
        if self.user_.is_authenticated():
            # 获取数据库中当前用户的购物车商品信息
            self.pl.hgetall('cart_%s' % self.user_.id)
            # 获取数据库中当前用户的购物车商品勾选信息
            self.pl.smembers('cart_selected_%s' % self.user_.id)
            # 管道执行 -- 返回结果
            result = self.pl.execute()
            # 购物车商品信息
            dict_cart = result[0]
            # 购物车商品勾选信息
            list_cart_selected = result[1]

            # 拼装字典 -- 循环购物车商品信息, sku_id: 商品id, count: 数量
            for sku_id, count in dict_cart.items():
                # 当前购物车商品
                self.cart[int(sku_id)] = {
                    # 商品数量
                    'count': int(count),
                    # 是否选择 -- 判断当前商品是否在商品勾选信息中
                    'selected': sku_id in list_cart_selected
                }
        # 未登陆用户 -- 数据存储在cookie
        else:
            # 如果有cookie购物车数据
            if self.cookie_cart:
                self.cart = self.cookie_cart

        # 查询购物车中所有的商品
        skus = SKU.objects.filter(id__in=self.cart.keys())
        # 循环sku列表, 添加两个字段: 商品数量和勾选状态
        for sku in skus:
            # sku当前购物车中的数量
            sku.count = self.cart[sku.id]['count']
            # sku当前购物车中是否勾选状态
            sku.selected = self.cart[sku.id]['selected']

        # 响应序列化数据
        serializer = CartSKUSerializer(skus, many=True)
        # 返回响应
        return Response(serializer.data)

    def post_action(self):
        """新增购物车数据"""

        # 如果是已登录用户 -- 数据存储在Redis
        if self.user_.is_authenticated():
            # 添加购物车商品信息, 如果已有数据, 数量相加
            self.pl.hincrby('cart_%s' % self.user_.id, self.sku_id, self.count)
            # 如果商品为勾选状态
            if self.selected:
                # 添加购物车商品勾选信息
                self.pl.sadd('cart_selected_%s' % self.user_.id, self.sku_id)
            # 管道执行
            self.pl.execute()
            # 返回响应
            return Response(self.serializer.data, status=status.HTTP_201_CREATED)
        # 未登陆用户 -- 数据存储在cookie
        else:
            # 如果有cookie购物车数据
            if self.cookie_cart:
                # 获取cookie中购物车商品信息
                sku = self.cookie_cart.get(self.sku_id)
                # 如果有商品信息
                if sku:
                    # 请求数量 + 购物车商品数量
                    self.count += int(sku.get('count'))

            # 封装购物车商品信息 -- 封装请求参数
            self.cookie_cart[self.sku_id] = {
                # 数量
                'count': self.count,
                # 是否勾选
                'selected': self.selected
            }

            # 字典 --> base64字符串
            cart_ = base64.b64encode(pickle.dumps(self.cookie_cart)).decode()
            # 返回数据, 201状态码
            response = Response(self.serializer.data, status=201)
            # 设置cookie保存购物车信息, 参数3 = cookie有效期
            response.set_cookie('cart', cart_, constants.CART_COOKIE_EXPIRES)
            # 返回响应
            return response

    def put_action(self):
        """修改购物车数据"""

        # 如果是已登录用户 -- 数据存储在Redis
        if self.user_.is_authenticated():
            # 修改商品数量
            self.pl.hset('cart_%s' % self.user_.id, self.sku_id, self.count)
            # 如果勾选状态为True
            if self.selected:
                # 添加购物车商品勾选信息
                self.pl.sadd('cart_selected_%s' % self.user_.id, self.sku_id)
            else:
                # 删除购物车商品勾选信息
                self.pl.srem('cart_selected_%s' % self.user_.id, self.sku_id)
            # 管道执行
            self.pl.execute()
            # 返回响应
            return Response(self.serializer.data)
        # 未登陆用户 -- 数据存储在cookie
        else:
            # 修改cookie购物车的商品信息
            self.cookie_cart[self.sku_id] = {
                # 数量
                'count': self.count,
                # 是否勾选状态
                'selected': self.selected
            }

            # 字典 --> base64字符串
            cart_ = base64.b64encode(pickle.dumps(self.cookie_cart)).decode()
            # 返回数据, 状态200
            response = Response(self.serializer.data)
            # 设置cookie保存购物车信息, 参数3 = cookie有效期
            response.set_cookie('cart', cart_, constants.CART_COOKIE_EXPIRES)
            # 返回响应
            return response

    def delete_action(self):
        """删除购物车数据"""

        # 如果是已登录用户 -- 数据存储在Redis
        if self.user_.is_authenticated():
            # 删除购物车商品信息
            self.pl.hdel('cart_%s' % self.user_.id, self.sku_id)
            # 删除购物车商品勾选信息
            self.pl.srem('cart_selected_%s' % self.user_.id, self.sku_id)
            # 管道执行
            self.pl.execute()
            # 返回响应
            return Response(status=status.HTTP_204_NO_CONTENT)
        # 未登陆用户 -- 数据存储在cookie
        else:
            # 实例化响应 状态码204
            response = Response(status=status.HTTP_204_NO_CONTENT)
            # 如果cookie中有购物车信息
            if self.cookie_cart:
                # 如果商品在cookie购物车中
                if self.sku_id in self.cookie_cart:
                    # 删除cookie购物车中的商品数据
                    del self.cookie_cart[self.sku_id]
                    # 字典 --> base64字符串
                    cart_ = base64.b64encode(pickle.dumps(self.cookie_cart)).decode()
                    # 设置cookie保存购物车信息, 参数3 = cookie有效期
                    response.set_cookie('cart', cart_, constants.CART_COOKIE_EXPIRES)
            # 返回响应
            return response

    def run(self):
        """运行函数

        :return:
        """
        # 获取动作小写属性
        action = self.action.lower()  # type: str
        # 如果动作不在指定属性中
        if not action in ["get", "post", "put", "delete"]:
            # action属性错误, 返回404
            return Response({"message": "action属性错误"}, status=status.HTTP_404_NOT_FOUND)
        # 通过action构成表达式
        # action_fun = eval("self." + action + "_action()")  # 可以指定在eval中执行函数"()"
        action_fun = eval("self." + action + "_action")
        # 返回运行结果
        return action_fun()


def merge_cart_cookie_to_redis(request, response, user):
    """合并cookie中的购物车数据到redis中

    :param request: 请求对象, 用于获取cookie
    :param response: 响应对象,用于清除cookie
    :param user: 登录用户, 用于获取用户id
    :return:
    """
    # 获取cookie购物车数据(base64字符串)
    cookie_cart = request.COOKIES.get('cart')
    # 如果没有数据
    if not cookie_cart:
        # 直接返回
        return response

    # base64字符串 --> 字典  --  cookie购物车信息
    # {2: {'count':1, 'selected':False}, 3: {'count':1, 'selected':False}}
    cookie_cart = pickle.loads(base64.b64decode(cookie_cart.encode()))

    # 合并cookie数据到redis中, 如果cookie和redis中存在相同的商品,则以cookie中的为准
    # 连接数据库
    redis_conn = get_redis_connection('cart')
    # 生成管道
    pl = redis_conn.pipeline()
    # 循环cookie中的购物车信息
    for sku_id, dict_count_selected in cookie_cart.items():
        # cookie中商品数量
        count = dict_count_selected['count']
        # cookie中商品勾选状态
        selected = dict_count_selected['selected']
        # 数据库添加
        pl.hset('cart_%s' % user.id, sku_id, count)
        # 如果当前商品为勾选
        if selected:
            # 添加购物车商品勾选数据
            pl.sadd('cart_selected_%s' % user.id, sku_id)
        else:
            # 删除购物车商品勾选数据
            pl.srem('cart_selected_%s' % user.id, sku_id)
    # 管道执行
    pl.execute()
    # 清除cookie数据
    response.delete_cookie('cart')
    # 返回响应
    return response
