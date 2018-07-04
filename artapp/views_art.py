from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from artapp.models import ArtTag, Art


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
    arts = Art.objects.filter(title=request.POST.get('searchKey'))
    return render(request,
                  'art/list_search.html',
                  {'arts': arts})
