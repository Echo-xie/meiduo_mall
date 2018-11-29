"""子应用视图

"""
import functools
import json

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View


def index(request):
    """首页

    :param request: 请求报文
    :return: 响应体
    """
    # 返回响应
    return HttpResponse("Hello World!!!<br>你好!!!")


def index_pk(request, pk):
    """首页带路径参数pk

    :param request: 请求报文
    :param pk: 主键
    :return: 响应体
    """
    # 返回字符串
    return_str = "pk = %s" % pk
    # 返回响应
    return HttpResponse(return_str)


def index_query(request):
    """首页带查询参数

    :param request: 请求报文
    :return: 响应体
    """
    # 获取查询参数
    a = request.GET.get("a", "无")
    b = request.GET.get("b", "无")
    a_list = request.GET.getlist("a", "无")
    # 返回字符串
    return_str = "查询参数"
    return_str += "<br>a = %s" % a
    return_str += "<br>b = %s" % b
    return_str += "<br>a_list = %s" % a_list

    # 返回响应
    return HttpResponse(return_str)


def index_post(request):
    """首页带表单参数

    :param request: 请求报文
    :return: 响应体
    """
    # 获取表单参数
    a = request.POST.get("a", "无")
    b = request.POST.get("b", "无")
    a_list = request.POST.getlist("a", "无")
    # 返回字符串
    return_str = "表单参数"
    return_str += "<br>a = %s" % a
    return_str += "<br>b = %s" % b
    return_str += "<br>a_list = %s" % a_list

    # 返回响应
    return HttpResponse(return_str)


def index_json(request):
    """首页带json参数

    :param request: 请求报文
    :return: 响应体
    """
    # 获取请求体
    json_str = request.body
    # 转码
    json_str = json_str.decode()  # python3.6 无需执行此步
    # 转类型
    req_data = json.loads(json_str)
    a = req_data.get("a", "无")
    b = req_data.get("b", "无")
    # 返回字符串
    return_str = "表单参数"
    return_str += "<br>a = %s" % a
    return_str += "<br>b = %s" % b

    # 返回响应
    return HttpResponse(return_str)


def reverse_index(request):
    """反编译 -- 首页

    :param request: 请求报文
    :return: 响应体
    """
    # 返回字符串
    return_str = "反编译\n"
    # 拼接字符串
    return_str += reverse("demo:demo_index")
    # 输出提示
    print(return_str)
    # 返回响应 -- 重定向到反编译的url
    return redirect(reverse("demo:demo_index"))


def reverse_index_pk(request, pk):
    """反编译 -- 首页带路径参数pk

    :param request: 请求报文
    :param pk: 主键
    :return: 响应体
    """
    # 返回字符串
    return_str = "反编译\n"
    # 拼接字符串  --  如果反编译的url是带有路径参数的, 需要用args 或 kwargs
    return_str += reverse("demo:demo_index_pk", args=pk)
    # return_str += reverse("demo:demo_index_pk", kwargs={"pk": pk})
    # 输出提示
    print(return_str)
    # 返回响应
    return redirect(reverse("demo:demo_index_pk", args=pk))


def reverse_index_query(request):
    """反编译 -- 首页带查询参数

    :param request: 请求报文
    :return: 响应体
    """
    # 获取查询参数
    a = request.GET.get("a", "无")
    b = request.GET.get("b", "无")
    a_list = request.GET.getlist("a", "无")
    # 返回字符串
    return_str = "反编译<br>"
    # 拼接字符串
    return_str += reverse("demo:demo_index_query")
    # 拼接字符串  --  如url需查询参数, 需手动拼接, 注意1key多value的情况
    return_str += "?a=%s&b=%s&a=%s" % (a, b, a_list)
    # 输出提示
    print(return_str)
    # 返回响应
    return redirect(reverse("demo:demo_index_query") + "?a=%s&b=%s&a=%s" % (a, b, a_list))


def my_decorator(func):
    """装饰器

    :param func: 装饰函数
    :return: 返回内函数
    """

    # 保留原函数名
    @functools.wraps(func)
    # 装饰函数 -- 执行装饰步骤
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了')
        print('请求路径%s' % request.path)
        # 返回原函数 -- 继续执行被装饰函数
        return func(request, *args, **kwargs)

    # 返回内函数
    return wrapper


class RegisterView(View):
    """注册类视图
    同一请求url, 路由进入此类, 根据不同请求方式[GET请求, POST请求, ...]调用不同的函数,
    类函数中, 命名必须以请求方式命名[get, post, ...]
    """

    @method_decorator(my_decorator)  # 为get方法添加了装饰器
    def get(self, request):
        """get请求

        :param request: 请求报文
        :return: 响应体
        """
        return HttpResponse("注册类视图GET请求返回")

    def post(self, request):
        """post请求

        :param request: 请求报文
        :return: 响应体
        """
        return HttpResponse("注册类视图POST请求返回")


def template_index(request):
    """首页模板

    :param request: 请求报文
    :return: 响应体
    """
    context = {
        'content': '首页模板 -- Hello World',
    }
    return render(request, 'template_index.html', context)
