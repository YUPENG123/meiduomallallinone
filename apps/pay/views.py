from alipay import AliPay
from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.orders.models import OrderInfo
from apps.pay.models import Payment
from meiduo_mall import settings
from utils.response_code import RETCODE

"""

1. 沙箱 appid

2. 沙箱网关

3. 沙箱应用私钥

4. 沙箱支付宝公钥


axirmj7487@sandbox.com


1. 我们需要去创建 2对公钥和私钥
    一对是我们的
    另外一对是支付宝的

"""


"""
生成电脑网站支付的连接 需要让前端传递订单id
我们需要 生成支付的连接

0.接收验证订单
1.创建alipay实例对象
2.生成order_string
3.拼接调转的url
4.返回

GET     payment/(?P<order_id>\d+)/

"""
from utils.views import LoginRequiredJSONMixin
class PaymentView(LoginRequiredJSONMixin,View):

    def get(self,request,order_id):
        # 0.接收验证订单
        try:
            # 传一个订单id是没有问题的
            # 为了让查询的更准确, 我们是应该查询 未支付的
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=request.user,
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return http.JsonResponse({'code':RETCODE.PARAMERR,'errmsg':'暂无此订单'})
        # 1.创建alipay实例对象
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()


        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug = True  # 默认False
        )
        # 2.生成order_string
        # 如果你是 Python 3的用户，使用默认的字符串即可
        subject = "测试订单"

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # 正式环境的 https://openapi.alipay.com/gateway.do? + order_string
        # 沙箱环境的 https://openapi.alipaydev.com/gateway.do
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject=subject,
            return_url=settings.ALIPAY_RETURN_URL,

        )
        # 3.拼接调转的url
        pay_url = settings.ALIPAY_URL + '?' + order_string
        # 4.返回
        return http.JsonResponse({'code':RETCODE.OK,'pay_url':pay_url})

class PayStatusView(View):

    def get(self,request):

        """
        将订单id和支付宝id保存起来

        1.创建支付宝实例
        2.获取验证数据
        3.根据状态保存数据
        """
        #
        # 1.创建支付宝实例
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        # 2.获取验证数据
        data = request.GET.dict()
        # sign 不能参与签名验证
        signature = data.pop("sign")

        # verify
        success = alipay.verify(data, signature)
        if success:
            # 3.根据状态保存数据
            """
            trade_no	String	必填	64	支付宝交易号	2013112011001004330000121536
            out_trade_no	String	必填	64	商户订单号	6823789339978248
            """
            trade_no = data.get('trade_no')
            out_trade_no=data.get('out_trade_no')

            Payment.objects.create(
                order_id=out_trade_no,
                trade_id=trade_no
            )


        return render(request,'pay_success.html',context={'trade_no':trade_no})
