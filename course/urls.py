
from django.conf.urls import url

from course.views import UrlView

urlpatterns = [
    url(r'^url', UrlView.as_view()),
]

