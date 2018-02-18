
from django.conf.urls import url

from landing.views import LandingView

urlpatterns = [
    url(r'^get', LandingView.as_view()),
]


