from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from artapp.models import ArtTag,Art

def index(request):



    # 返回渲染模板
    return render(request, 'art/list.html',
                  context={'art':Art.objects.all(),
                           'tags': ArtTag.objects.all()})


def add_tags(request):
    # 添加标签类型的处理函数
    if request.method == 'GET':
        # 新增,修改
        # 判断是否为修改
        id = request.GET.get('id')
        tag = None
        if id:
            # 存在id,即为修改
            tag = ArtTag.objects.get(id=id)
        return render(request, 'art/edit_tags.html', {'tag': tag})
    else:
        # POST请求
        # 新增,修改
        if request.POST.get('id'):
            tag = ArtTag.objects.get(id=request.POST.get('id'))
        else:
            tag = ArtTag()
        tag.title = request.POST.get('title')
        tag.save()  # 保存到数据库中
        return redirect('/art/list_tags')   # 重定向


def delete_tag(request):
    id = request.GET.get('id')
    if id:
        result = ArtTag.objects.filter(id=id)
        if result.exists():
            result.delete()
    # 重定向到列表页面
    return redirect('/art/list_tags')

def list_tags(request):
    return render(request,
                  'art/tags_list.html',
                  context={
                      'tags': ArtTag.objects.all()
                  })

