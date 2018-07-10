from DjangoUeditor.models import UEditorField
from django.db import models


# 小说或文章标签类型
class ArtTag(models.Model):
    title = models.CharField(max_length=20,
                             verbose_name='作品类别',
                             unique=True)
    add_time = models.DateTimeField(verbose_name='添加的时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)

    class Meta:
        verbose_name = '分类标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 小说文章的模型
class Art(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='文章名')
    # 作者(模型,建立多对一的关联关系)
    author = models.CharField(max_length=50, blank=True, verbose_name='作者')
    summary = UEditorField(verbose_name='概述',
                           default='',
                           blank=True,
                           width=680,  # 编辑页面显示的宽度
                           height=640,  # 编辑页面显示的高度
                           toolbars='full',  # 工具栏的按钮
                           imagePath='ueditor/images/',  # 上传图片的路径（正文中）
                           filePath='ueditor/files/',  # 上传文件的路径
                           )
    # imgurl = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images',
                            verbose_name='文章的图片',
                            default='http://www.freexs.org/modules/article/images/nocover.jpg',
                            blank=True,  # 内容可以为空
                            null=True)

    counter = models.IntegerField(default=0, verbose_name='阅读次数')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    # 文章类型(一端)
    tag = models.ForeignKey(ArtTag,
                            on_delete=models.SET_NULL,
                            null=True,
                            verbose_name='分类')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

# 文章小节模型

