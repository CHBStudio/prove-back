
from django.conf.urls import url

from payment.views import UrlView

urlpatterns = [
    url(r'^url', UrlView.as_view()),
]
