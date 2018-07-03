from django.db import models


class ArtTag(models.Model):
    title = models.CharField(max_length=20,
                             verbose_name='作品类别',
                             unique=True)
    add_time = models.DateTimeField(verbose_name='添加的时间',auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='最后修改时间',auto_now=True)




