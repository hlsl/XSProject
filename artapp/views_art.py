import time
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.cache import cache_page
from django.template import loader  # 导入模块加载器, 可以渲染模板
from artapp.models import ArtTag, Art
from django.core.cache import cache  # django的核心包


# 声明针对相关请求的处理函数
def art_edit(request):

    if request.method == 'GET':
        return render(request,
                  'art/edit_art.html',
                  {'tags':ArtTag.objects.all()})
    elif request.method == 'POST':  # post请求
        title = request.POST.get('title').strip()
        author = request.POST.get('author')
        summary = request.POST.get('summary')
        tag_id = request.POST.get('tag')

        # 获取上传的文件
        artImg:InMemoryUploadedFile = request.FILES.get('artImg')

        # print(title, author, tag_id)
        # print(summary)
        # print(request.FILES)
        # print(artImg)

        errors = {}
        # 验证数据
        if not title:
            errors['title'] = '标题不能为空'
        elif len(title) > 50:
            errors['title'] = '长度不能超出50个字符'

        if not author:
            errors['author'] = '作者不能为空'
        elif len(title) > 20:
            errors['author'] = '长度不能超出20个字符'

        # 判断验证是否存在错误
        if len(errors) > 0:
            return render(request,
                          'art/edit_art.html',
                          {'tags':ArtTag.objects.all(),
                           'errors':errors})

        # 保存数据
        art = Art()
        art.title = title
        art.author = author
        art.summary = summary
        art.img = artImg
        art.tag_id = tag_id
        art.save()

        return redirect('/art/')


def search(request):
    # 按书名或作者名搜索
    skey = request.POST.get('searchKey')
    arts = Art.objects.filter(Q(title__contains=skey) | Q(author__contains=skey))

    # 作业: 分页和页面布局

    return render(request,
                  'art/list_search.html',
                  {'arts': arts})


# 将页面缓存到redis中
# @cache_page(10)
def show(request):

    id = request.GET.get('id')  # 请求参数中的数据, str
    print('--show id--', id)

    # 1.先从缓存中读取(key设计: Art-1)
    page = cache.get('Art-%s' % id)
    if not page:
        time.sleep(5)

        # 3.1 查询文章信息
        art = Art.objects.get(id=id)

        # 3.2 加载模板文件,并渲染成html文本
        page = loader.render_to_string('art/art_info.html', {'art': art})

        # 4. 将加载完成后的页面存放到cache中
        # key, value, timeout
        cache.set('Art-%s' % id, page, 10)

    return HttpResponse(page)
