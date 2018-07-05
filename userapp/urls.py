from django.conf.urls import url

from userapp import views

urlpatterns = [
    # 声明用户请求
    url(r'^regist', views.regist),
    url(r'upload', views.upload),

]