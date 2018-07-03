class Check():
    def __init__(self, func):
        print('-------创建Check对象-----')
        self.func = func  # 当使用装饰类时, 会创建装饰类对象

    # 创建完Check类对象后, 则会直接调用__call__, 且将被装饰函数参数传入到__call__
    def __call__(self, *args, **kwargs):
        print('正在检查用户权限')
        return self.func(*args, **kwargs)

@Check   # 引用的是check类,  而不是其类的对象, 但是将被包装的函数时传入到__init__
def remove(bookId):
    print('正在删除:' , bookId)
#-------创建Check对象-----

remove(101)
remove(102)

'''
正在检查用户权限
正在删除: 101
正在检查用户权限
正在删除: 102
'''





