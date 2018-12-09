from django.contrib import admin
from . import models
from celery_tasks.html.tasks import generate_static_list_search_html
from celery_tasks.html.tasks import generate_static_sku_detail_html


class GoodsCategoryAdmin(admin.ModelAdmin):
    """自定义管理admin站点 -- 商品类别"""

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


class SKUAdmin(admin.ModelAdmin):
    """自定义管理admin站点 -- sku具体商品"""

    def save_model(self, request, obj, form, change):
        """admin后台新增或修改了数据时调用"""

        obj.save()
        # 生成静态页面 -- sku详情页面
        generate_static_sku_detail_html.delay(obj.id)


class SKUSpecificationAdmin(admin.ModelAdmin):
    """自定义管理admin站点 -- sku具体商品具体规格"""

    def save_model(self, request, obj, form, change):
        """admin后台新增或修改了数据时调用"""

        obj.save()
        # 生成静态页面 -- sku详情页面
        generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self, request, obj):
        """admin后台删除了数据时调用"""

        sku_id = obj.sku.id
        obj.delete()
        # 生成静态页面 -- sku详情页面
        generate_static_sku_detail_html.delay(sku_id)


class SKUImageAdmin(admin.ModelAdmin):
    """自定义管理admin站点 -- sku图片"""

    def save_model(self, request, obj, form, change):
        """admin后台新增或修改了数据时调用"""

        obj.save()
        # 生成静态页面 -- sku详情页面
        generate_static_sku_detail_html(obj.sku.id)

        # 判断sku是否有默认图片, 如果没有, 则在新增商品图片时进行设置
        sku = obj.sku
        # 判断图片为空
        if not sku.default_image_url:
            # 设置商品默认图片
            sku.default_image_url = obj.image.url
            sku.save()

    def delete_model(self, request, obj):
        """admin后台删除了数据时调用"""

        sku_id = obj.sku.id
        obj.delete()
        generate_static_sku_detail_html(sku_id)


# 商品类别
admin.site.register(models.GoodsCategory, GoodsCategoryAdmin)
# SKU具体规格
admin.site.register(models.SKUSpecification, SKUSpecificationAdmin)
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
admin.site.register(models.SKU, SKUAdmin)
# SKU图片
admin.site.register(models.SKUImage, SKUImageAdmin)
