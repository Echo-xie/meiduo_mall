from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from areas.areas_serializers import AreaSerializer
from areas.models import Area


class AreaListView(APIView):
    """获取省市区管理列表"""

    # @cache_response(timeout=60 * 60, cache='default')
    def get(self, request, parent):
        """获取省市区管理列表
        根据pk获取外键为pk的列表 -- 市 或 区
        如果pk为0获取外键为空的列表 -- 省
        :param request:
        :param parent: 外键
        :return:
        """
        # 如果parent为0
        if parent == "0":
            # 赋值为空
            parent = None
        # 根据parent获取列表
        area_list = Area.objects.filter(parent=parent)
        # 设置序列化器, 列表要设置many为True
        area_s = AreaSerializer(area_list, many=True)
        # 返回
        return Response(area_s.data)
