from django.contrib.auth.models import User, AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import SessionAuthentication

from user.models import AuthToken


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request, *args, **kwargs):
        if request.path.startswith('/admin') is False:
            header_token = request.COOKIES.get('Authorization', None)
            if header_token is not None:
                try:
                    token = AuthToken.objects.get(key=header_token)
                    request.user = token.user
                except AuthToken.DoesNotExist:
                    pass
            else:
                request.user = AnonymousUser()

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
