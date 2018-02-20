import hashlib

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from proxy.views import proxy_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from app.decorators import login_required
from app.views import NoCSRFView
from course.models import Course, Exercise, Schedule
from course.serializer import CourseSerializer, ExerciseSerializer
from prove import settings
from prove.settings import MERCHANT_LOGIN, PASSWORD1


class ListView(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        courses = Course.objects.filter(users__in=[user]).order_by('order')
        response = []
        if courses:
            for course in courses:
                course = CourseSerializer(course).data
                c = {
                    'title': course.title,
                    'is_active': course.active,
                    'description': course.description,
                    'photo': course.photo,

                }
                response.append(c)
        return Response(data={
            'courses': response
        })


class GetView(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        course_id = request.GET.get('id')
        try:
            course = Course.objects.get(id=course_id, users__in=[user])

        except Course.DoesNotExist:
            raise PermissionError
        resp = []
        schedules = Schedule.objects.filter(course_id=course.id)
        for sc in schedules:
            exercises = Exercise.objects.filter(schedule=sc).order_by('order')
            resp.append({
                'day':sc.day,
                'exercises':ExerciseSerializer(exercises,many=True).data
            })

        course = CourseSerializer(course).data
        return Response(data={
            'course': course,
            'schedule':resp
        })


class UrlView(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request):
        course_id = request.GET.get('id')
        course = Course.objects.get(id=course_id)
        cost = course.cost
        SignatureValue = hashlib.md5(
            '{}:{}:{}:{}:Shp_course={}'.format(MERCHANT_LOGIN, cost, request.user.id, PASSWORD1, course_id).encode(
                'utf-8')).hexdigest()
        url = 'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={}&OutSum={}&InvId={}&SignatureValue={}&Shp_course={}'.format(
            MERCHANT_LOGIN, cost, request.user.id, SignatureValue, course_id)

        return HttpResponseRedirect(redirect_to=url)


class CheckPerm(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        path = request.path.replace('/media/', '')
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
        path = request.path.replat('/media', '')
        id = request.GET.get('course_id')
        if id:
            course = Exercise.objects.get(video=path).schedule.course
            if user in course.users.all():
                secret = settings.SECRET_HASH
                remoteurl = 'http://127.0.0.1/{}'.format(secret) + request.path
                return proxy_view(request, remoteurl)
            else:
                raise NotFound
