"""手动生成所有sku的静态页面

date: 18-12-9 下午10:16
"""

import sys
import os
import django

# 添加导包路径 (把 scripts 的上一级目录添加到导包路径sys.path)
sys.path.insert(0, '../')

# 设置当前脚本运行配置文件, 初始化django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")
# Django预备
django.setup()

# 需先添加导包路径后再添加项目路径
from celery_tasks.html.tasks import generate_static_sku_detail_html
from goods.models import SKU

# 功能逻辑, 具体执行功能
if __name__ == '__main__':
    # 获取所有sku数据
    skus = SKU.objects.all()
    # 循环sku
    for sku in skus:
        print(sku.id)
        # 生成当前sku静态页面
        generate_static_sku_detail_html(sku.id)
