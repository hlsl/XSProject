from django.conf.urls import url
<<<<<<< HEAD
from artapp.views import *
=======
>>>>>>> huyz

from artapp import views_art
from artapp.views import *

urlpatterns = [
    # 声明主页面的请求
    url(r'^tags', add_tags),
    url(r'^list_tags', list_tags),
    url(r'^delete_tag', delete_tag),
<<<<<<< HEAD:artapp/urls.py
<<<<<<< HEAD
    url('^', index),
=======
    url(r'^art_edit$', views_art.art_edit),
=======
    url(r'^art_edit$', views_art.art_edit),  # 编辑文章
>>>>>>> huyz:apps/artapp/urls.py
    url(r'^search', views_art.search),  # 搜索文章
    url(r'^show', views_art.show),
    url(r'^sendMsg', views_art.sendMsg),
    url('^$', index),
>>>>>>> huyz
]