"""订单子应用 -- 工具

date: 18-12-13 下午7:21
"""
from django_redis import get_redis_connection


def get_orders_goods(request):
    """获取下单商品
    :param request: 请求报文
    """

    # 获取当前用户对象
    user = request.user
    # 数据库连接
    redis_conn = get_redis_connection('carts')
    # 获取用户购物车商品数据 -- cart_1 = {1:2, 2:2} [k=sku_id, v=数量]
    redis_cart = redis_conn.hgetall('cart_%s' % user.id)
    # 获取用户购物车商品选中状态 -- cart_selected_1 = {1, 2} [v=sku_id]
    cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)

    # 下单商品
    cart = {}
    # 循环用户购物车商品选中的商品
    for sku_id in cart_selected:
        # 根据选中的商品获取商品信息, 添加至下单商品
        cart[int(sku_id)] = int(redis_cart[sku_id])

    # 返回下单商品
    return cart
