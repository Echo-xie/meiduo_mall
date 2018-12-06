from django.contrib import admin

from . import models

# 商品类别
admin.site.register(models.GoodsCategory)
# SKU具体规格
admin.site.register(models.SKUSpecification)
# 商品频道
admin.site.register(models.GoodsChannel)
# 品牌
admin.site.register(models.Brand)
# 商品SPU
admin.site.register(models.Goods)
# 商品规格
admin.site.register(models.GoodsSpecification)
# 规格选项
admin.site.register(models.SpecificationOption)
# 商品SKU
admin.site.register(models.SKU)
# SKU图片
admin.site.register(models.SKUImage)
