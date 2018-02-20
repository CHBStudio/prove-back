
from django.conf.urls import url

from course.views import UrlView

urlpatterns = [
    url(r'^pay', UrlView.as_view()),
]

