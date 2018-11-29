"""应用配置

"""
from django.apps import AppConfig

class TestDemoConfig(AppConfig):
    """子应用配置

    """
    # 包名
    name = 'test_demo'
    # 详情名称 -- 在admin管理中显示的名称
    verbose_name = '测试模块'