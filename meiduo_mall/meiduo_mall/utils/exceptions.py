"""捕获DRF未处理的异常

date: 18-11-29 下午10:47
"""
from rest_framework.response import Response
from rest_framework.views import exception_handler
import logging

# 实例化日志类
logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    """捕获DRF未处理的异常

    :param exc: 异常
    :param context: 正文
    :return: 响应体
    """
    # 调用DRF的异常处理函数exception_handler, 接收返回 Response对象
    response = exception_handler(exc, context)
    # 如果返回对象为空, 表示出现未处理异常
    if response is None:
        # 处理异常: 捕获异常并保存至日志文件中
        # 出错视图
        view = context['view']
        # 错误信息
        error = '服务器内部错误： %s，%s' % (view, exc)
        # 写日志
        logger.error(error)
        # 返回响应体
        return Response({'message': error}, status=500)
    # 返回响应
    return response
