from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from meiduo_mall.utils.models import BaseModel


class GoodsCategory(BaseModel):
    """商品类别"""
    name = models.CharField(max_length=10, verbose_name='名称')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父类别')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_goods_category'
        # 详情名称
        verbose_name = '商品类别'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsChannel(BaseModel):
    """商品频道"""
    group_id = models.IntegerField(verbose_name='组号')
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='一级商品类别')
    url = models.CharField(max_length=50, verbose_name='频道页面链接')
    sequence = models.IntegerField(verbose_name='组内顺序')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_goods_channel'
        # 详情名称
        verbose_name = '商品频道'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name


class Brand(BaseModel):
    """品牌"""
    name = models.CharField(max_length=20, verbose_name='名称')
    logo = models.ImageField(verbose_name='Logo图片')
    first_letter = models.CharField(max_length=1, verbose_name='品牌首字母')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_brand'
        # 详情名称
        verbose_name = '品牌'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """商品SPU"""
    name = models.CharField(max_length=50, verbose_name='名称')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌')
    category1 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat1_goods', verbose_name='一级类别')
    category2 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat2_goods', verbose_name='二级类别')
    category3 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat3_goods', verbose_name='三级类别')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评价数')

    # desc_detail = models.TextField(default='', verbose_name='详细介绍')
    # desc_pack = models.TextField(default='', verbose_name='包装信息')
    # desc_service = models.TextField(default='', verbose_name='售后服务')

    # 使用富文本编辑器类型[RichTextUploadingField: 支持文件上传, RichTextField: 不支持文件上传]
    desc_detail = RichTextUploadingField(default='', verbose_name='详细介绍')
    desc_pack = RichTextField(default='', verbose_name='包装信息')
    desc_service = RichTextUploadingField(default='', verbose_name='售后服务')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_goods'
        # 详情名称
        verbose_name = '商品'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSpecification(BaseModel):
    """商品规格"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    name = models.CharField(max_length=20, verbose_name='规格名称')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_goods_specification'
        # 详情名称
        verbose_name = '商品规格'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.goods.name, self.name)


class SpecificationOption(BaseModel):
    """规格选项"""
    spec = models.ForeignKey(GoodsSpecification, on_delete=models.CASCADE, verbose_name='规格')
    value = models.CharField(max_length=20, verbose_name='选项值')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_specification_option'
        # 详情名称
        verbose_name = '规格选项'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s - %s' % (self.spec, self.value)


class SKU(BaseModel):
    """商品SKU"""
    name = models.CharField(max_length=50, verbose_name='名称')
    caption = models.CharField(max_length=100, verbose_name='副标题')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, verbose_name='从属类别')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='进价')
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市场价')
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评价数')
    is_launched = models.BooleanField(default=True, verbose_name='是否上架销售')
    default_image_url = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name='默认图片')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_sku'
        # 详情名称
        verbose_name = '商品SKU'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class SKUImage(BaseModel):
    """SKU图片"""
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='sku')
    image = models.ImageField(verbose_name='图片')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_sku_image'
        # 详情名称
        verbose_name = 'SKU图片'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.sku.name, self.id)


class SKUSpecification(BaseModel):
    """SKU具体规格"""
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='sku')
    spec = models.ForeignKey(GoodsSpecification, on_delete=models.PROTECT, verbose_name='规格名称')
    option = models.ForeignKey(SpecificationOption, on_delete=models.PROTECT, verbose_name='规格值')

    class Meta:
        """元数据"""
        # 指定数据库表
        db_table = 'tb_sku_specification'
        # 详情名称
        verbose_name = 'SKU规格'
        # 详情名称复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s - %s' % (self.sku, self.spec.name, self.option.value)
