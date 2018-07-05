from django.shortcuts import render


def regist(request):
    return render(request, 'user/regist.html')