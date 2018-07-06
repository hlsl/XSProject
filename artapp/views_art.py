import time
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import loader  # 导入模块加载器, 可以渲染模板
from artapp.models import ArtTag, Art
from django.core.cache import cache  # django的核心包
from artapp.urils import cache_page, rds


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
@cache_page(5)
def show(request):

    id = request.GET.get('id')  # 请求参数中的数据, str
    # print('--show id--', id)
    # 查询文章信息
    art = Art.objects.get(id=id)

    # 修改文章的浏览次数
    art.counter += 1
    art.save()

    # redis数据存储(非cache)
    # 每次阅读都累加
    rds.zincrby('Rank-Art', id)

    return render(request, 'art/art_info.html', {'art': art})


def top5Art(request):
    # (<Art (1)>, 3900)
    # 1. 从redis中读取前5的排行
    rank_art = rds.zrevrange('Rank-Art', 0, 4, withscores=True)
    rank_ids = [ id.decode() for id,_ in rank_art]

    # 根据ids列表,查询所有数据,并返回字典
    # key : id
    # value: Art类的对象
    arts = Art.objects.in_bulk(rank_ids)

    # 最终获取的阅读排行数据: [(<Art object>, socre),...]
    top_arts = [(arts.get(int(id.decode())), score) for id, score in rank_ids]

    return top_arts
