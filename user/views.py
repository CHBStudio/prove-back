from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.exceptions import AuthenticationFailed, ParseError, NotFound, ValidationError, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.decorators import login_required
from app.middleware import CsrfExemptSessionAuthentication
from app.utils import generate_token
from app.views import NoCSRFView
from user.models import AuthToken
from user.serializer import UserSerializer


class TestView(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request, format=None):
        return Response(headers={
            'Cookie': 'Autorza'
        }, data='ok')


class LoginView(NoCSRFView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
                if user and user.check_password(password):
                    token = generate_token(email=email, password=password, user_id=user.id)
                    userializer = UserSerializer(user)
                    return Response(headers={
                        'Set-Cookie': 'Authorization={}; Path=/'.format(token)
                    },
                        data={
                            'user': userializer.data
                        })

                else:
                    raise AuthenticationFailed
            except User.DoesNotExist:
                raise NotFound
        else:
            raise ParseError


class RegisterView(NoCSRFView):

    def post(self, request):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        password = request.data.get('password')
        if email and password and first_name:
            try:
                user = User.objects.get(email=email)
                raise ValidationError(detail='Email not unique')
            except User.DoesNotExist:
                user = User(
                    email=email,
                    first_name=first_name,
                    password=make_password(password)
                ).save()
                user = User.objects.get(email=email)
                userializer = UserSerializer(user)
                token = generate_token(email=email, password=password, user_id=user.id)
                return Response(headers={
                    'Set-Cookie': 'Authorization={}; Path=/'.format(token)
                },
                    data={
                        'user': userializer.data
                    })
        else:
            raise ParseError


class LogoutView(NoCSRFView):

    def post(self, request):
        user = request.user
        if user.pk:
            AuthToken.objects.get(user=user).delete()
            return Response(data={
                'status': 'ok'
            })
        else:
            raise NotAuthenticated


class GetView(NoCSRFView):

    def get(self, request):
        user = request.user
        if user.pk:
            return Response(data={
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                data={
                    'user': None
                }
            )
