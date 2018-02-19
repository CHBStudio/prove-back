
from django.conf.urls import url

from payment.views import PaymentView

urlpatterns = [
    url(r'^new', PaymentView.as_view()),
]
