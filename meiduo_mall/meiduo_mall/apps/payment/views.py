from alipay import AliPay
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import OrderInfo
from payment.models import Payment


class AliPaymentView(APIView):
    """支付接口 -- 跳转阿里支付
    GET payment/alipay/(?P<order_id>\d+)/
    """

    # 读取商家私钥和阿里公钥
    alipay_public_key_string = open("meiduo_mall/apps/payment/keys/alipay_public_key.pem").read()
    app_private_key_string = open("meiduo_mall/apps/payment/keys/app_private_key.pem").read()

    # 用户验证
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """获取阿里支付url"""
        try:
            # 根据订单号, 当前登陆用户, 支付方式, 订单状态, 获取订单 -- 判断订单信息是否正确
            order = OrderInfo.objects.get(order_id=order_id, user=request.user,
                                          pay_method=OrderInfo.PAY_METHODS_ENUM["ALIPAY"],
                                          status=OrderInfo.ORDER_STATUS_ENUM["UNPAID"])
        except OrderInfo.DoesNotExist:
            return Response({'message': '订单信息有误'}, status=status.HTTP_400_BAD_REQUEST)
        # 实例化阿里支持对象
        alipay = AliPay(
            # 指定支付宝应用的id
            appid=settings.ALIPAY_APPID,
            # 支付成功后支付宝会重定向到此地址, 没有指定支付成功不会跳转
            app_notify_url="http://www.meiduo.site:8080/pay_success.html",
            # 商家私钥
            app_private_key_string=AliPaymentView.app_private_key_string,
            # 支付宝的公钥, 验证支付宝回传消息使用
            alipay_public_key_string=AliPaymentView.alipay_public_key_string,
            # 加密算法, 使用RSA2
            sign_type="RSA2",
            # 默认False
            debug=settings.ALIPAY_DEBUG
        )

        # 发起支付请求
        order_string = alipay.api_alipay_trade_page_pay(
            # 订单id
            out_trade_no=order_id,
            # 注意需要转成字符串, 否则会出错!
            total_amount=str(order.total_amount),
            # 主题
            subject="美多商城 %s" % order_id,
            # 同步返回url -- 支付成功后阿里跳转
            return_url="http://www.lnsist.top:8080/pay_success.html",
            # 异步返回url -- 支付成功后阿里异步发送支付结果
            notify_url="http://api.lnsist.top:8000/payment/notify"
        )

        # 跳转阿里支付页面
        alipay_url = settings.ALIPAY_URL + "?" + order_string
        # 返回
        return Response({'alipay_url': alipay_url})

    def put(self, request):
        """处理支付结果
        -- 如果url带有查询参数的请求是同步支付返回请求, 否则是异步支付返回请求
        1. 修改订单状态: 待支付 -> 待发货
        2. payment表保存支付成功的订单id,支付宝id
        """

        # 标记是否异步返回 -- 默认False
        is_asyn = False
        # 获取url查询参数
        data = request.query_params.dict()
        # 如果没有url查询参数
        if not data:
            # 获取请求体参数
            data = request.data.dict()

        # 移除并获取sign -- sign是签名部分, 移除后剩下的数据要进行校验, 获取sign用于校验
        signature = data.pop("sign")

        # 实例化阿里支持对象
        alipay = AliPay(
            # 指定支付宝应用的id
            appid=settings.ALIPAY_APPID,
            # 支付成功后支付宝会重定向到此地址, 没有指定支付成功不会跳转
            app_notify_url=None,
            # 商家私钥
            app_private_key_string=AliPaymentView.app_private_key_string,
            # 支付宝的公钥, 验证支付宝回传消息使用
            alipay_public_key_string=AliPaymentView.alipay_public_key_string,
            # 加密算法, 使用RSA2
            sign_type="RSA2",
            # 默认False
            debug=settings.ALIPAY_DEBUG
        )

        # 验签: 用sign校验剩下的数据是否合法和完整 -- 校验支付宝平台返回的支付结果数据
        result = alipay.verify(data, signature)
        # 如果校验通过 -- 表示数据是合法的且没有没篡改过的
        if result:
            # 获取订单id
            order_id = data.get('out_trade_no')
            # 获取支付宝支付流水号: 交易id
            trade_id = data.get('trade_no')
            # 订单支付成功, 保存订单id和交易id
            Payment.objects.create(order_id=order_id, trade_id=trade_id)

            # 修改订单状态为: 待发货 -- 乐观锁
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']) \
                .update(status=OrderInfo.ORDER_STATUS_ENUM["UNSEND"])

            # 三目运算 -- 如果当前请求是异步返回前面的HttpResponse, 否则后面的Response
            response = HttpResponse('success') if is_asyn else Response({'trade_id': trade_id})
            # 返回
            return response

        # 校验不通过
        else:
            # 返回
            return Response({'message': '非法请求'}, status=status.HTTP_403_FORBIDDEN)
