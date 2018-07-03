from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    # 请求路径和请求方法
    print(request.path, request.method)
    # 请求头的元信息和GET请求参数(查询参数)
    # print(request.META, request.GET)
    print(request.GET)
    print(request.GET.get('page'), request.GET.get('tag'))
    # POST请求参数(表单参数)
    print(request.POST)
    # return HttpResponse('<h1>您好</h1>')
    # return JsonResponse({'name': 'huyz', 'age': 20})
    return render(request, 'art/list.html', context={'name': 'huyz', 'age': 20})




