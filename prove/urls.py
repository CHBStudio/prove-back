from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app.views import LandingView
from prove import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('rest_auth.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^payment/', include('payment.urls')),
    url(r'^landing/get', LandingView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

