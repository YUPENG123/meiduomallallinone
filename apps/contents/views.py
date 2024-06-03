from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.contents.models import ContentCategory
from apps.contents.utils import get_categories

"""

1.首页经常被访问到,首页的数据经常会被查询到,所以我们想到的是 将首页的数据进行redis的缓存操作
    以减少数据库的查询

2. 页面静态化

    我们让用户直接去访问静态的html,但是静态的html的数据 必须是数据库(业务逻辑)中最新的

    我们如何去实现静态化呢?

    ①我们可以先查询数据库,然后将查询的数据渲染到html中,将这个html写入到指定文件
    当用户访问的时候直接去访问就可以

    ②问题: 什么时候去重新生成静态化页面
        我们采用定时任务

"""
class IndexView(View):

    def get(self,request):
        """
         # 1.分类信息
         # 2.楼层信息
        """
        # 1.分类信息 分类信息在其他页面也会出现,我们应该直接抽取为一个方法
        # 查询商品频道和分类
        categories = get_categories()

        # 2.楼层信息
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }

        return render(request,'index.html',context=context)

"""
一对一
    2个表(不考虑自关联)
    例如: 个人常用信息 和 个人不常用信息


一对多
    2个表
    例如: 品牌和商品
        用户和订单  一个用户有多个订单


多对多
    3个表

    老师和学生

    老师id    老师名字
    1111        明
    2222        齐


    学生id    学生名字

    666         张三
    999         李四



    学生id       老师id
    666         1111
    666         2222
    999          1111
    999         2222

    商品和供应商

    商品id    商品名字

    8888        iphone
    9999         华为


    供应商id   供应商名字
    1000        富士康
    2000        付土康


    商品id       供应商id
    8888        1000
    8888        2000
    9999        2000
    9999        1000


"""



#1.导入
# from fdfs_client.client import Fdfs_client
#
# #2.创建客户端实例,加载指定配置文件
# client = Fdfs_client('utils/fdfs/client.conf')
#
# #3.上传图片
# # filename 写绝对路径
# client.upload_by_filename('/home/python/Desktop/images/mei.png')
# client.upload_by_filename('long.png')

# class IndexView(View):
#
#     def get(self,request):
#
#
#         return render(request,'index.html')