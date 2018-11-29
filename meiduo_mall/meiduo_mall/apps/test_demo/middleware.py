"""demo_test中间件

"""


def my_middleware(get_response):
    """中间件函数
    结构和装饰器函数一致

    :param get_response:
    :return:
    """
    # 初始化时调用
    print('init 被调用')

    def middleware(request):
        """每个请求处理前,
        在具体路由视图函数执行前

        :param request:
        :return:
        """
        print('before request 被调用')
        # 执行视图函数
        response = get_response(request)
        print('after response 被调用')
        return response

    return middleware


def my_middleware2(get_response):
    """中间件函数
    结构和装饰器函数一致

    :param get_response:
    :return:
    """
    # 初始化时调用
    print('init 2 被调用')

    def middleware(request):
        """每个请求处理前,
        在具体路由视图函数执行前

        :param request:
        :return:
        """
        print('before request 2 被调用')
        # 执行视图函数
        response = get_response(request)
        print('after response 2 被调用')
        return response

    return middleware
