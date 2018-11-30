from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


def index(request):
    """用户视图 -- 首页

    :param request:
    :return:
    """
    return HttpResponse("Hello World!!!")


def test(request):
    """模板测试

    :param request:
    :return:
    """
    return render(request, "cross_domain_test.html")


class cross_domain_test(APIView):
    """跨域请求测试

    """

    def get(self, request):
        return Response({"message": "get请求"})

    def post(self, request):
        return Response({"message": "post请求"})
