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
from course.user_in_course import UsersInCourse
from prove.settings import VK_CLIENT_ID, REDIRECT_URL, VK_CLIENT_SECRET, FB_CLIENT_ID, FB_REDIRECT_URL, FB_CLIENT_SECRET
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
                    username=email,
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
            return Response(
                data={
                    'user': None
                }
            )

        else:
            raise NotAuthenticated


class GetView(NoCSRFView):

    def get(self, request):
        user = request.user
        if user.pk:
            userdata = UserSerializer(user).data
            courses = user.course_set.all()
            courseslist = []
            for c in courses:
                days = c.expire
                userincourse = UsersInCourse.objects.get(course=c, user=user)
                if userincourse.check_time(days) is None:
                    userincourse.delete()
                else:
                    courseslist.append(c.id)
            userdata['courses'] = courseslist
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

    def get(self, request):
        code = request.GET.get('code')
        url = 'https://oauth.vk.com/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}'.format(
            VK_CLIENT_ID,
            VK_CLIENT_SECRET,
            REDIRECT_URL,
            code
        )
        data = requests.get(url)
        data = data.json()
        access_token = data.get('access_token')
        user_id = data.get('user_id')
        user_url = 'https://api.vk.com/method/users.get?access_token=4a9be6044a9be6044a9be604434afa87dc44a9b4a9be604101605ecda0a16e0ca46f3c2&user_ids={}&fields=bdate&v=5.73'.format(
            user_id)
        userdata = requests.get(user_url)
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
        return Response(status=302,
                        headers={
                            'Set-Cookie': 'Authorization={}; Path=/'.format(token),
                            'Location': '/'
                        },

                        data={
                            'user': user
                        })


class FBView(NoCSRFView):

    def get(self, request):
        url = """https://www.facebook.com/v2.12/dialog/oauth?client_id={}&redirect_uri={}&state=bhjsdfghkjsgfhjsdbafkbhj""".format(
            FB_CLIENT_ID, FB_REDIRECT_URL)
        return HttpResponseRedirect(redirect_to=url)


class FBAuthView(NoCSRFView):

    def get(self, request):
        code = request.GET.get('code')
        url = """https://graph.facebook.com/v2.12/oauth/access_token?client_id={}&redirect_uri={}&client_secret={}&code={}""".format(
            FB_CLIENT_ID,
            FB_REDIRECT_URL,
            FB_CLIENT_SECRET,
            code
        )
        data = requests.get(url)
        data = data.json()
        access_token = data.get('access_token')
        user_url = 'https://graph.facebook.com/me?fields=first_name,last_name&access_token={}'.format(access_token)
        userdata = requests.get(user_url)
        userdata = userdata.json()
        user_id = userdata.get('id')
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
        return Response(status=302,
                        headers={
                            'Set-Cookie': 'Authorization={}; Path=/'.format(token),
                            'Location': '/'
                        },

                        data={
                            'user': user
                        })
