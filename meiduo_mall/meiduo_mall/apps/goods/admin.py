from django.contrib import admin
from . import models


class GoodsCategoryAdmin(admin.ModelAdmin):
    """自定义管理admin站点"""

    def save_model(self, request, obj, form, change):
        """admin后台新增或修改了数据时调用"""

        # 数据保存
        obj.save()
        # 导包
        from celery_tasks.html.tasks import generate_static_list_search_html
        # 生成静态页面
        generate_static_list_search_html.delay()

    def delete_model(self, request, obj):
        """admin后台删除了数据时调用"""

        # 数据删除
        obj.delete()
        # 导包
        from celery_tasks.html.tasks import generate_static_list_search_html
        # 生成静态页面
        generate_static_list_search_html.delay()


# 商品类别
admin.site.register(models.GoodsCategory, GoodsCategoryAdmin)
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
