
from django.conf.urls import url

from user.views import LoginView, GetView, RegisterView, LogoutView

urlpatterns = [
    url(r'^login', LoginView.as_view()),
    url(r'^get', GetView.as_view()),
    url(r'^register', RegisterView.as_view()),
    url(r'^logout', LogoutView.as_view()),

]
