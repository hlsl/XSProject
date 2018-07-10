import xadmin
from xadmin import views
from artapp.models import ArtTag, Art


class BaseSetting():
    # 启用主题样式选择
    enable_themes = True

    # 切换菜单
    use_bootswatch = True


class GlobalSettings(object):
    # 配置站点标题
    site_title = '美文管理后台'

    # 配置站点底部版本信息和友情链接
    site_footer = '<em style="font-size:20px">千锋教育</em><br>@版本所有 ·深圳Python1802'

    menu_style = 'accordion'

    # 配置全局检索的模型
    global_search_models = (ArtTag, Art)

    # 配置全局模型显示的图标
    global_models_icon = {
        ArtTag: 'glyphicon glyphicon-th',
        Art: 'glyphicon glyphicon-list-alt',
    }


class ArtTagAdmin():
    list_display = ('title',)
    search_fields = ('title',)


class ArtAdmin():
    list_display = ('title', 'summary', 'author', 'img', 'publish_time', 'tag')
    search_fields = ('title', 'author')

    # 配置每页显示的记录数
    list_per_page = 3

    style_fields = {'summary': 'ueditor'}

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

# 向xadmin后台注册模型类
xadmin.site.register(Art, ArtAdmin)
xadmin.site.register(ArtTag, ArtTagAdmin)