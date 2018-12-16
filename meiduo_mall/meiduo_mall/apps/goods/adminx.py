"""xadmin后台站点管理 -- goods

list_display        控制列表展示的字段
search_fields       控制可以通过搜索框搜索的字段名称，xadmin使用的是模糊查询
list_filter         可以进行过滤操作的列
ordering            默认排序的字段
readonly_fields     在编辑页面的只读字段
exclude             在编辑页面隐藏的字段
list_editable       在列表页可以快速直接编辑的字段
show_detail_fileds  在列表页提供快速显示详情信息
refresh_times       指定列表页的定时刷新
list_export         控制列表页导出数据的可选格式
show_bookmarks      控制是否显示书签功能
data_charts         控制显示图标的样式
model_icon          控制菜单的图标

date: 18-12-16 上午7:14
"""

import xadmin
from xadmin import views

from . import models
from celery_tasks.html.tasks import generate_static_list_search_html
from celery_tasks.html.tasks import generate_static_sku_detail_html


class BaseSetting(object):
    """自定义xadmin的基本配置"""

    # 开启主题切换功能
    enable_themes = True
    # 使用启动样本
    use_bootswatch = True


# 站点注册
xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """自定义xadmin的全局配置"""

    # 设置站点标题
    site_title = "美多商城运营管理系统"
    # 设置站点的页脚
    site_footer = "美多商城集团有限公司"
    # 设置菜单折叠
    menu_style = "accordion"


# 站点注册
xadmin.site.register(views.CommAdminView, GlobalSettings)


class SKUAdmin(object):
    """自定义sku站点管理"""

    model_icon = 'fa fa-gift'
    list_display = ['id', 'name', 'price', 'stock', 'sales', 'comments']
    list_filter = ['category']
    list_editable = ['price', 'stock']
    show_detail_fields = ['name']
    show_bookmarks = True
    list_export = ['xls', 'csv', 'xml']
    refresh_times = [3, 5]  # 可选以支持按多长时间(秒)刷新页面
    readonly_fields = ['sales', 'comments']

    def save_models(self):
        """admin后台新增或修改了数据时调用"""

        obj = self.new_obj
        obj.save()
        # 生成静态页面 -- sku详情页面
        generate_static_sku_detail_html.delay(obj.id)


class SKUSpecificationAdmin(object):
    def save_models(self):
        # 保存数据对象
        obj = self.new_obj
        obj.save()

        # 补充自定义行为
        generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self):
        # 删除数据对象
        obj = self.obj
        sku_id = obj.sku.id
        obj.delete()

        # 补充自定义行为
        generate_static_sku_detail_html.delay(sku_id)


class GoodCategorysAdmin(object):
    """自定义管理admin站点 -- 商品类别"""

    def save_models(self):
        """admin后台新增或修改了数据时调用"""

        obj = self.new_obj
        # 数据保存
        obj.save()
        # 生成静态页面 -- 商品列表页面[list.html] 和 搜索商品页面[search.html]
        generate_static_list_search_html.delay("list.html")
        generate_static_list_search_html.delay("search.html")

    def delete_models(self):
        """admin后台删除了数据时调用"""

        obj = self.obj
        # 数据删除
        obj.delete()
        # 生成静态页面 -- 商品列表页面[list.html] 和 搜索商品页面[search.html]
        generate_static_list_search_html.delay("list.html")
        generate_static_list_search_html.delay("search.html")


class SKUImageAdmin(object):
    """自定义管理admin站点 -- sku图片"""

    def save_models(self):
        """admin后台新增或修改了数据时调用"""

        obj = self.new_obj
        obj.save()
        # 生成静态页面 -- sku详情页面
        generate_static_sku_detail_html.delay(obj.sku.id)

        # 判断sku是否有默认图片, 如果没有, 则在新增商品图片时进行设置
        sku = obj.sku
        # 判断图片为空
        if not sku.default_image_url:
            # 设置商品默认图片
            sku.default_image_url = obj.image.url
            sku.save()

    def delete_models(self):
        """admin后台删除了数据时调用"""

        obj = self.obj
        sku_id = obj.sku.id
        obj.delete()
        generate_static_sku_detail_html.delay(sku_id)


# 商品类别
xadmin.site.register(models.GoodsCategory, GoodCategorysAdmin)
# SKU具体规格
xadmin.site.register(models.SKUSpecification, SKUSpecificationAdmin)
# 商品频道
xadmin.site.register(models.GoodsChannel)
# 品牌
xadmin.site.register(models.Brand)
# 商品SPU
xadmin.site.register(models.Goods)
# 商品规格
xadmin.site.register(models.GoodsSpecification)
# 规格选项
xadmin.site.register(models.SpecificationOption)
# 商品SKU
xadmin.site.register(models.SKU, SKUAdmin)
# SKU图片
xadmin.site.register(models.SKUImage, SKUImageAdmin)
