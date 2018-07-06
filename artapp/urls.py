from django.conf.urls import url

from artapp import views_art
from artapp.views import *

urlpatterns = [
    # 声明主页面的请求
    url(r'^tags', add_tags),
    url(r'^list_tags', list_tags),
    url(r'^delete_tag', delete_tag),
    url(r'^art_edit$', views_art.art_edit),
    url(r'^search', views_art.search),  # 搜索文章
    url(r'^read', views_art.read),  # 阅读
    url('^$', index),
]