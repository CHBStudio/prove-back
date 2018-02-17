from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from app.decorators import login_required
from app.middleware import CsrfExemptSessionAuthentication
from course.models import Course
from course.serializer import CourseSerializer


class NoCSRFView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)


class LandingView(NoCSRFView):

    def get(self, request, format=None):
        user = request.user
        courseslist = []
        courses = Course.objects.all().order_by('order')
        for course in courses:
            course_json = CourseSerializer(course).data
            course_json['has_permissions'] =  True if user.pk and user in course.users.all() else False
            courseslist.append(course_json)

        return Response(data={
            'courses': courseslist
        })
