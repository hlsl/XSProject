
# 声明一个view处理函数的装饰器
import time
from django.core.cache import cache
from django.http import HttpRequest
from django.http import HttpResponse
from redis import Redis

from artapp.models import Art

rds = Redis(host='10.36.137.61', db=2, password='redis')


def cache_page(timeout):
    def wrapper_view(view_func):
        def wrapper(request:HttpRequest, *args, **kwargs):
            url = request.get_full_path()
            # 1. 根据url请求路径从缓存中读取内容
            page = cache.get(url)
            if not page:  # 缓存中不存在,则执行请求处理函数
                # time.sleep(5)
                response: HttpResponse = view_func(request)

                # 将响应的内容存放到缓存中
                cache.set(url, response.content, timeout)
                return response
            else:
                return HttpResponse(page)

        return wrapper
    return wrapper_view


# 获取前5的阅读排行
def top5Art():
    # 1. 从redis中读取前5的排行
    # [(b'5', 3.0), (b'1', 2.0),...]
    rank_art = rds.zrevrange('Rank-Art', 0, 4, withscores=True)

    rank_ids = [id.decode() for id,_ in rank_art]

    # 根据ids列表，查询所有数据，并返回字典
    # key : id
    # value: Art类的对象
    # {1:<Art object>, 2:<Art object>}
    arts = Art.objects.in_bulk(rank_ids)

    # 最终获取的阅读排行数据:  [ (<Art object>, socre), ...]
    top_arts = [(arts.get(int(id.decode())), score) for id, score in rank_art]

    return top_arts


