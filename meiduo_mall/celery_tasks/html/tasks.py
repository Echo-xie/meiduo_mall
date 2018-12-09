"""celery执行具体任务 -- 生成静态页面

date: 18-12-8 上午10:07
"""
from celery_tasks.main import celery_app
from django.template import loader
from django.conf import settings
import os
from contents.crons import get_categories
from goods.models import SKU


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


@celery_app.task(name='generate_static_sku_detail_html')
def generate_static_sku_detail_html(sku_id):
    """生成商品详情静态页面<br>
    此函数是通过点击[sku]{具体商品}进入的,
    但是展示的数据其实是[spu]{商品}的数据,
    所以需要通过[sku]获取对应的[spu]数据,
    然后获取[spu]的所有规格数据,
    最后对比当前[sku]的规格数据,
    页面进行高亮显示
    :param sku_id: 商品sku id
    """
    """
        [sku] = 具体商品
        [spu] = 商品
    """

    # 获取商品分类
    categories = get_categories()

    # 获取当前[sku]信息
    sku = SKU.objects.get(id=sku_id)
    # 获取[sku]的所有图片
    sku.images = sku.skuimage_set.all()

    # 获取当前[sku]的[spu]信息
    goods = sku.goods
    # 获取商品频道 -- 根据商品类别 [一级类别 才对应有频道]
    goods.channel = goods.category1.goodschannel_set.all()[0]

    # 获取当前[sku]的规格信息 -- 排序规格ID
    sku_specs = sku.skuspecification_set.order_by('spec_id')
    # 封装当前[sku]的规格选项
    sku_key = []
    # 循环当前[sku]规格信息 -- [获取当前[sku]的所有规格选项]
    for spec in sku_specs:
        # 添加规格选项ID
        sku_key.append(spec.option.id)

    # 获取当前[spu]的所有[sku]
    skus = goods.sku_set.all()

    # 封装所有[sku]的规格信息字典
    # -- k: [sku]的所有规格选项, v: 是哪个[sku]
    spec_sku_map = {}
    # 循环当前[spu]的所有[sku]
    # -- [获取[spu]的所有[sku]的规格信息, 因为需要通过[sku]获取对应规格信息]
    for s in skus:
        # 获取[sku]的规格信息
        s_specs = s.skuspecification_set.order_by('spec_id')
        # 封装所有[sku]的规格选项字典key
        key = []
        # 循环[sku]的规格信息
        for spec in s_specs:
            # 添加当前[sku]规格信息的规格选项
            key.append(spec.option.id)
        # tuple转为元组, 元组不可修改
        # 添加当前[sku]的所有规格选项
        spec_sku_map[tuple(key)] = s.id

    # 获取当前[spu]商品规格 -- 排序规格ID
    specs = goods.goodsspecification_set.order_by('id')

    # 若当前[sku]的规格信息不完整, 则不再继续
    if len(sku_key) < len(specs):
        return

    # enumerate: 将可迭代对象添加索引
    # 循环当前[spu]商品规格 -- [对比所有[sku]规格信息]
    for index, spec in enumerate(specs):
        # 复制当前[sku]的规格选项 （复制列表中的所有元素, 得到一个新的列表, :表示切片操作）
        key = sku_key[:]
        # 获取当前商品规格的所有规格选项
        options = spec.specificationoption_set.all()
        # 循环规格选项 -- 设置当前规格选项指向哪个[sku]
        for option in options:
            # 设置当前规格选项ID
            key[index] = option.id
            # 设置当前规格选项的sku -- 对比所有sku的规格选项, 没有则为None
            option.sku_id = spec_sku_map.get(tuple(key))
        # 设置当前商品规格指向哪个规格选项
        spec.options = options

    # 封装页面内容, 渲染模板, 生成静态html文件
    context = {
        # 商品类别
        'categories': categories,
        # 商品, 当前[sku]的[spu]
        'goods': goods,
        # 当前[sku]的[spu]所有规格
        'specs': specs,
        # 当前[sku]的详情信息
        'sku': sku
    }
    # 获取模板
    template = loader.get_template('detail.html')
    # 渲染模板内容
    html_text = template.render(context)
    # 生成静态页面
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'goods/' + str(sku_id) + '.html')
    # 将渲染内容写入静态页面
    with open(file_path, 'w') as f:
        # 写入数据
        f.write(html_text)
