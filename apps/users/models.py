from django.db import models

# Create your models here.

"""
1. 自己定义模型
    class User(models.Model):
        username=
        password=
        mobile=

    密码是明文,我们自己要完成验证 等等一些问题

2. 我们发现我们在学习基础的时候 django自带了 admin后台管理
    admin 后台管理 也有用户信息的保存和认证 密码是密文,也可以验证用户信息

   我们就想用户 django自带的用户模型


"""
from django.contrib.auth.models import AbstractUser

"""
当系统的类/方法不能满足我们需求的时候,我们就继承/重写
"""
class User(AbstractUser):

    mobile=models.CharField(max_length=11,unique=True,verbose_name='手机号')

    email_active = models.BooleanField(default=False,verbose_name='邮箱激活状态')

    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# class Person(object):
#
#     name = ''
#     sex = ''
#     age =''
#
#
# class Man(Person):
#
#     weigth=''
#
#     pass


"""
我想在每个表中 都有2个字段 一个是创建时间 一个是修改时间

"""

from utils.models import BaseModel

class Address(BaseModel):
    """用户地址"""
    # related_name='addresses' 默认就是 关联模型类名_set

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']

