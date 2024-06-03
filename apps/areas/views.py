from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.areas.models import Area
from utils.response_code import RETCODE

"""
省市区

    id      name        parent_id

    10000   河北省         NULL


    10100   保定市        10000
    10200   石家庄市      10000


    10101   雄县          10100
    10102   安新          10100


省的数据
    select * from tb_areas where parent_id is NULL;

市/区县
    select * from tb_areas where parent_id=130000;
    select * from tb_areas where parent_id=130600;

"""
# class ShengView(View):
#
#     def get(self,request):
#         pass
#
# class ShiQuXianView(View):
#     def get(self,request,parent_id):
#         pass


# areas/?parent_id=xxxx


# areas/   获取省的信息
# areas/?parent_id=xxxx 市/区县信息

"""
当我们的数据在一定时间内不经常发生变化
我们的数据会经常被查询到

我们可以将我们的数据放到缓存中,以减少mysql的查询


1W 用户产生了查询 1s

缓存优化
1W 9999个用了缓存  1个查询数据库

"""
from django.core.cache import cache
class AreasView(View):

    def get(self,request):

        # parent_id = request.GET.get('parent_id')
        parent_id = request.GET.get('area_id')
        if parent_id is None:

            # 先获取缓存
            provience_list = cache.get('pro')
            if provience_list is None:

                # 查询 省的信息
                proviences = Area.objects.filter(parent_id=None)
                # [Area,Area,Area]
                # 使用Vue去渲染数据
                # 我们是通过ajax 来返回相应
                # 我们需要将 对象转换为字典数据
                # proviences = Area.objects.filter(parent__parent_id__isnull=True)

                provience_list = []
                for item in proviences:
                    provience_list.append({
                        'id':item.id,
                        'name':item.name
                    })


                # 把转换的数据保存到缓存中
                # cache.set(key,value,expire)
                cache.set('pro',provience_list,24*3600)

            return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok','province_list':provience_list})

        else:
            # 查询 市/区县信息
            sub_list = cache.get('sub_%s'%parent_id)

            if sub_list is None:

                sub_areas = Area.objects.filter(parent_id=parent_id)
                # [Area,Area,Area]

                sub_list = []
                for sub in sub_areas:
                    sub_list.append({
                        'id':sub.id,
                        'name':sub.name
                    })

                cache.set('sub_%s'%parent_id,sub_list,24*3600)

            return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok','sub_data':sub_list})

