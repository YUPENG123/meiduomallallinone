from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^payment/(?P<order_id>\d+)/$',views.PaymentView.as_view(),name='payment'),
    url(r'^payment/status/$',views.PayStatusView.as_view(),name='paystatus'),
]