from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=50, verbose_name='用户名')
    # django的密码生成器生成 make_password
    password = models.CharField(max_length=100, verbose_name='密码')
    phone = models.CharField(max_length=13, verbose_name='手机号码', null=True, blank=True)
    # upload_to 指定的路径是相对于setting.py中设置的MEDIA_ROOT的路径
    photo = models.ImageField(upload_to='users', verbose_name='头像', null=True)
    # 注册时间
    regist_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    # 最近登录时间
    login_time = models.DateTimeField(auto_now=True, verbose_name='最近登录时间')

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户信息'

    def save(self):
        # 会出现什么问题? 修改个人信息时,密码会被再次加密
        # 解决办法 : 判断密码是否为密文,如果不是密文,则生成
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save()

    # 登陆时,验证口令是否正确
    # 前提,先通过用户查询用户,如果用户存在,再验证密码
    def varify_passwd(self, password):
        # 验证密码是否一致
        return check_password(password, self.password)
