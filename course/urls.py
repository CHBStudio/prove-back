
from django.conf.urls import url

from course.views import UrlView, ListView, GetView

urlpatterns = [
    url(r'^pay', UrlView.as_view()),
    url(r'^list', ListView.as_view()),
    url(r'^get', GetView.as_view()),
]

