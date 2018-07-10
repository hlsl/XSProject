import time

import logging
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import loader  # 导入模块加载器, 可以渲染模板

from artapp import tasks
from artapp.models import ArtTag, Art
from django.core.cache import cache  # django的核心包
from artapp.urils import cache_page, rds, top5Art
from XSProject.settings import logger


# 声明针对相关请求的处理函数

def art_edit(request):

    if request.method == 'GET':
        return render(request,
                      'art/edit_art.html',
                      {'tags': ArtTag.objects.all()})
    else:  # post请求
        # strip()去除两边空格
        title = request.POST.get('title').strip()
        author = request.POST.get('author').strip()
        summary = request.POST.get('summary').strip()
        tag_id = request.POST.get('tag').strip()

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
                          {'tags': ArtTag.objects.all(),
                           'errors': errors})

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
    print(skey)
    arts = Art.objects.filter(Q(title__contains=skey) | Q(author__contains=skey))

    return render(request,
                  'art/list_search.html',
                  {'arts': arts})


# 将页面缓存到redis中
@cache_page(5)
def show(request):
    id = request.GET.get('id')  # 请求参数中的数据, str类型
    # formatter = '%(asctime)s: %(filename)s.%(funcName)s at %(lineno)s->%(message)'
    #
    # # 配置日志的信息,filename表示要指定日志输出的文件名
    # logging.basicConfig(format=formatter,
    #                     datefmt='%Y-%m-%d %H:%M:%S',
    #                     filename='art.log',
    #                     filemode='a')
    logging.warning('---当前页面要被缓存5秒---')
    # 查询文章信息
    art = Art.objects.get(id=id)

    # 修改文章的浏览次数
    art.counter += 1
    art.save()

    # redis数据存储(非cache)
    # 每次阅读都累加
    rds.zincrby('Rank-Art', id)

    return render(request,
                  'art/art_info.html',
                  {'art': art,
                  'top_arts': top5Art()})


def sendMsg(request):
    to = request.GET.get('to')
    msg = request.GET.get('msg')

    # 调用发送邮件的任务
    # delay是task的异步任务调用的函数
    tasks.sendMail.delay(to, msg)

    return JsonResponse({'status': 'ok',
                         'msg': '任务已安排'})
