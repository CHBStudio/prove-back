import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from rest_framework.exceptions import AuthenticationFailed, ParseError, NotFound, ValidationError, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.decorators import login_required
from app.middleware import CsrfExemptSessionAuthentication
from app.utils import generate_token
from app.views import NoCSRFView
from prove.settings import VK_CLIENT_ID, REDIRECT_URL, VK_CLIENT_SECRET
from user.models import AuthToken
from user.serializer import UserSerializer


class LoginView(NoCSRFView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
                if user and user.check_password(password):
                    token = generate_token(email=email, password=password, user_id=user.id)
                    userdata = UserSerializer(user).data
                    userdata['courses'] = list(user.course_set.values_list('id', flat=True))
                    return Response(headers={
                        'Set-Cookie': 'Authorization={}; Path=/'.format(token)
                    },
                        data={
                            'user': userdata
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
                user = userializer.data
                user['courses'] = []
                return Response(headers={
                    'Set-Cookie': 'Authorization={}; Path=/'.format(token)
                },
                    data={
                        'user': user
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
            userdata = UserSerializer(user).data
            userdata['courses'] = list(user.course_set.values_list('id', flat=True))
            return Response(data={
                'user': userdata
            })
        else:
            return Response(
                data={
                    'user': None
                }
            )


class VKView(NoCSRFView):

    def get(self, request):
        url = 'https://oauth.vk.com/authorize?client_id={}&display=page&redirect_uri={}&scope=friends&response_type=code&v=5.73'.format(
            VK_CLIENT_ID, REDIRECT_URL)
        return HttpResponseRedirect(redirect_to=url)


class VKAuthView(NoCSRFView):

    def get(self,request):
        code = request.GET.get('code')
        url = 'https://oauth.vk.com/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}'.format(
            VK_CLIENT_ID,
            VK_CLIENT_SECRET,
            REDIRECT_URL,
            code
        )
        data = requests.get(url)
        data = data.json()
        print(data)
        access_token = data.get('access_token')
        user_id = data.get('user_id')
        user_url = 'https://api.vk.com/method/users.get?user_ids={}&fields=bdate&v=5.73'.format(user_id)
        userdata = requests.get(user_url)
        print(userdata.json())
        userdata = userdata.json()['response'][0]
        first_name = userdata.get('first_name')
        last_name = userdata.get('last_name')
        username = str(user_id)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name
            ).save()
        user = User.objects.get(username=username)
        userializer = UserSerializer(user)
        token = generate_token(email=username, password=first_name, user_id=user.id)
        user = userializer.data
        user['courses'] = []
        return Response(headers={
            'Set-Cookie': 'Authorization={}; Path=/'.format(token)
        },
            data={
                'user': user
            })
