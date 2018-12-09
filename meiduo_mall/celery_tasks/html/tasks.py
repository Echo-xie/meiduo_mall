"""celery执行具体任务 -- 生成静态页面

date: 18-12-8 上午10:07
"""
from celery_tasks.main import celery_app
from django.template import loader
from django.conf import settings
import os
from contents.crons import get_categories


@celery_app.task(name='generate_static_list_search_html')
def generate_static_list_search_html(template_name):
    """生成静态的商品列表页和搜索结果页html文件
    :param template_name: 需要生成的模板名称
    """

    # 获取商品类别
    categories = get_categories()

    # 模板内容
    context = {
        # 商品类别
        'categories': categories,
    }

    # 获取模板
    # template = loader.get_template('list.html')
    template = loader.get_template(template_name)
    # 渲染模板内容
    html_text = template.render(context)

    # 生成静态页面
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, template_name)
    # 将渲染内容写入静态页面
    with open(file_path, 'w') as f:
        # 写入数据
        f.write(html_text)
