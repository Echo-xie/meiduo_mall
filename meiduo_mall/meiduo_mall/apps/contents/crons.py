"""定时任务

date: 18-12-8 上午9:08
"""
import datetime
from collections import OrderedDict
import os
from django.conf import settings
from django.template import loader
from contents.models import ContentCategory
from goods.models import GoodsChannel


def get_categories():
    """获取商品类别[三级联动]

    :return: 商品频道有序字典
    """
    # 实例有序字典
    ordered_dict = OrderedDict()
    # 排序获取商品频道列表 -- 分组ID, 权重
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')  # 37条
    # 循环
    for channel in channels:
        # 获取分组 -- 第n组[一级类别]
        group_id = channel.group_id
        # 如果当前分组不在字典中
        if group_id not in ordered_dict:
            # 初始化字典{一级类别属性列表, 子类别列表}
            group_dict = {'channels': [], 'sub_cats': []}
            # 有序字典赋值
            ordered_dict[group_id] = group_dict
        else:
            # 获取有序字典中的数据 -- 获取[一级类别]添加后续类别
            group_dict = ordered_dict[group_id]

        # 设置[一级类别属性]
        cat1 = channel.category
        # 类别对象url
        cat1.url = channel.url
        # 添加[一级类别]
        group_dict['channels'].append(cat1)

        # 根据[一级类别]获取对应[二级类别]
        for cat2 in cat1.goodscategory_set.all():
            # [二级类别]初始化子类别列表
            cat2.sub_cats = []
            # 根据[二级类别]获取对应[三级类别]
            for cat3 in cat2.goodscategory_set.all():
                # [二级列表]子类别添加[三级类别]
                cat2.sub_cats.append(cat3)
            # [一级类别]子类别添加[二级类别]
            group_dict['sub_cats'].append(cat2)
    # 返回商品频道有序字典
    return ordered_dict


def generate_static_index_html():
    """生成静态的index.html
    定时任务执行, 手动调用执行
    """

    # 记录执行时间
    print('%s: generate_static_index_html' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 获取商品类别数据
    ordered_dict = get_categories()
    # print(ordered_dict)

    # 广告类别字典初始化
    contents = {}
    # 获取全部广告类别
    content_categories = ContentCategory.objects.all()
    # 循环广告类别
    for cat in content_categories:
        # 主键表查询外键表[类名小写_set]
        # 广告类别key = 广告内容
        contents[cat.key] = cat.content_set.all().filter(status=True).order_by('sequence')

    # 模板内容
    context = {
        # 商品类别
        'categories': ordered_dict,
        # 广告类别
        'contents': contents
    }
    # 获取模板
    template = loader.get_template('index.html')
    # 渲染模板内容
    html_text = template.render(context)

    # 生成静态页面
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')
    # 将渲染内容写入静态页面
    with open(file_path, 'w') as f:
        # 写入数据
        f.write(html_text)
