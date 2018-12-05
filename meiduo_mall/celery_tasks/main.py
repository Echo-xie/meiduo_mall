"""

date: 18-12-1 下午8:40
"""
from celery import Celery
import os

# 设置配置文件, 需要放置到创建celery对象之前
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

# 创建celery对象
celery_app = Celery('meiduo')
# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 指定要扫描任务的包, 会自动读取包下的名字为 tasks.py 的文件
celery_app.autodiscover_tasks(['celery_tasks.sms', "celery_tasks.email"])
