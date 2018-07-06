from django.conf.urls import url

from userapp import views

urlpatterns = [
    # 用户注册请求
    url(r'^regist', views.regist),
    # 图片上传请求
    url(r'upload', views.upload),
    # 用户登陆请求
    url(r'^login', views.login),
    # 用户注销
    url(r'^logout', views.logout),

]