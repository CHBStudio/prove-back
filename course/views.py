import hashlib

from django.utils.decorators import method_decorator
from proxy.views import proxy_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from app.decorators import login_required
from app.views import NoCSRFView
from course.models import Course, Exercise
from prove import settings
from prove.settings import MERCHANT_LOGIN, PASSWORD1


class UrlView(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request):
        course_id = request.GET.get('id')
        course = Course.objects.get(id=course_id)
        cost = course.cost
        SignatureValue = hashlib.md5(
            '{}:{}:{}:{}:Shp_course={}'.format(MERCHANT_LOGIN, cost, request.user.id, PASSWORD1,course_id).encode('utf-8')).hexdigest()
        url = 'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={}&OutSum={}&InvId={}&SignatureValue={}&Shp_course={}'.format(
            MERCHANT_LOGIN, cost, request.user.id, SignatureValue,course_id)

        return Response(data={
            'url': url
        })

class CheckPerm(NoCSRFView):

    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        path = request.path.replace('/media/','')
        if id:
            course = Exercise.objects.get(video=path).schedule.course
            if user in course.users.all():
                secret = settings.SECRET_HASH
                remoteurl = 'http://127.0.0.1/{}'.format(secret) + request.path
                return proxy_view(request, remoteurl)
            else:
                raise NotFound

class CourseListView(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        path = request.path.replat('/media','')
        id = request.GET.get('course_id')
        if id:
            course = Exercise.objects.get(video=path).schedule.course
            if user in course.users.all():
                secret = settings.SECRET_HASH
                remoteurl = 'http://127.0.0.1/{}'.format(secret) + request.path
                return proxy_view(request, remoteurl)
            else:
                raise NotFound
