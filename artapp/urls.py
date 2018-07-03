from django.conf.urls import url
from artapp.views import *


urlpatterns = [
    # 声明主页面的请求
    url(r'^tags', add_tags),
    url(r'^list_tags', list_tags),
    url(r'^delete_tag', delete_tag),
    url('^', index),
]