
from django.conf.urls import url

from user.views import LoginView, GetView, RegisterView, LogoutView, VKView, VKAuthView

urlpatterns = [
    url(r'^login', LoginView.as_view()),
    url(r'^get', GetView.as_view()),
    url(r'^register', RegisterView.as_view()),
    url(r'^logout', LogoutView.as_view()),
    url(r'^vk-auth', VKAuthView.as_view()),
    url(r'^vk/$', VKView.as_view()),

]
