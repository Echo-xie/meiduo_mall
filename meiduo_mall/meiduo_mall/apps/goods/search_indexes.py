"""Haystack索引库

date: 18-12-9 下午5:24
"""
from haystack import indexes
from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引类"""

    # 定义搜索字段 -- 自动去模板加载搜索字段, 模板路径 templates/search/indexes/子应用名称/实体类名_text.txt
    text = indexes.CharField(document=True, use_template=True)

    # 需要保存在索引库中的字段
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.DecimalField(model_attr='price')
    default_image_url = indexes.CharField(model_attr='default_image_url')
    comments = indexes.IntegerField(model_attr='comments')

    def get_model(self):
        """获取模型实体类"""

        # 返回建立索引的模型类
        return SKU

    def index_queryset(self, using=None):
        """获取索引查询集"""

        # 返回要建立索引的数据查询集 -- 提供数据库数据, 生成索引
        return self.get_model().objects.filter(is_launched=True)
