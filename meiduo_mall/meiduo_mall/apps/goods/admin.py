from django.contrib import admin
from . import models
from celery_tasks.html.tasks import generate_static_list_search_html


class GoodsCategoryAdmin(admin.ModelAdmin):
    """自定义管理admin站点"""

    def save_model(self, request, obj, form, change):
        """admin后台新增或修改了数据时调用"""

        # 数据保存
        obj.save()
        # 生成静态页面 -- 商品列表页面[list.html] 和 搜索商品页面[search.html]
        generate_static_list_search_html.delay("list.html")
        generate_static_list_search_html.delay("search.html")

    def delete_model(self, request, obj):
        """admin后台删除了数据时调用"""

        # 数据删除
        obj.delete()
        # 生成静态页面 -- 商品列表页面[list.html] 和 搜索商品页面[search.html]
        generate_static_list_search_html.delay("list.html")
        generate_static_list_search_html.delay("search.html")


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
