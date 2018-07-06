
# 声明一个view处理函数的装饰器
import time
from django.core.cache import cache
from django.http import HttpRequest
from django.http import HttpResponse
from redis import Redis

rds = Redis(host='10.36.137.61', db='XSProject', password='redis')

def cache_page(timeout):
    def wrapper_view(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            url = request.get_full_path()
            # 1. 根据url请求路径从缓存中读取内容
            page = cache.get(url)
            if not page:
                time.sleep(5)
                response: HttpResponse = view_func(request)

                # 将响应的内容存放到缓存中
                cache.set(url, response.content, timeout)
                return response
            else:
                return HttpResponse(page)

        return wrapper
    return wrapper_view



