from django.conf.urls import url
from artapp import views


urlpatterns = [
    # 声明主页面的请求
    url('', views.index),
]