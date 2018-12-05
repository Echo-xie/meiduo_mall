"""分页配置类

date: 18-12-5 下午9:38
"""
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    # 默认每页显示2条
    page_size = 10
    # 查询关键字名称：第几页
    page_query_param = 'page'
    # 查询关键字名称：每页多少条
    page_size_query_param = 'page_size'
