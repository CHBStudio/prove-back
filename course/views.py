import hashlib
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from proxy.views import proxy_view
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from app.decorators import login_required
from app.views import NoCSRFView
from course.models import Course, Exercise, Schedule
from course.serializer import CourseSerializer, ExerciseSerializer
from course.user_in_course import UsersInCourse
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
                days = course.expire
                userincourse = UsersInCourse.objects.get(course=course, user=user)
                if userincourse.check_time(days) is None:
                    userincourse.delete()
                else:
                    course = CourseSerializer(course).data
                    c = {
                        'title': course.get("title"),
                        'is_active': course.get("active"),
                        'description': course.get("description"),
                        'photo': course.get("photo"),
                        'expired': userincourse.get_expire(days)
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
            days = course.expire
            userincourse = UsersInCourse.objects.get(course=course,user=user)
            if userincourse.check_time(days) is None:
                userincourse.delete()
                raise Course.DoesNotExist
        except Course.DoesNotExist:
            raise PermissionDenied
        resp = []
        schedules = Schedule.objects.filter(course_id=course.id).order_by('week')
        ws = [sc.week for sc in schedules]
        weeks = set(ws)
        for week in weeks:
            weeklist = []
            schedules = Schedule.objects.filter(course_id=course_id,week=week).order_by('day')
            for sc in schedules:
                exercises = Exercise.objects.filter(schedule=sc).order_by('order')
                weeklist.append({
                    'day': sc.day,
                    'exercises': ExerciseSerializer(exercises, many=True).data
                }
                )
            resp.append(weeklist)

        course = CourseSerializer(course).data
        course['expired'] = userincourse.get_expire(days)
        return Response(data={
            'course': course,
            'schedule': resp
        })


class UrlView(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request):
        course_id = request.GET.get('id')
        course = Course.objects.get(id=course_id)
        cost = course.cost
        cost = cost - cost * 0.0654
        SignatureValue = hashlib.md5(
            '{}:{}::{}:Shp_course={}:Shp_user={}'.format(MERCHANT_LOGIN, cost, PASSWORD1,
                                                         course_id,
                                                         request.user.id).encode(
                'utf-8')).hexdigest()
        url = 'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={}&OutSum={}&InvDesc={}&SignatureValue={}&Shp_course={}&Shp_user={}'.format(
            MERCHANT_LOGIN, cost, course.title, SignatureValue, course_id, request.user.id)

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
