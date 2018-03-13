from rest_framework.response import Response

from app.views import NoCSRFView
from course.models import Course
from course.serializer import CourseSerializer
from course.user_in_course import UsersInCourse
from landing.models import Faq, Result
from landing.serializer import FaqSerializer, ResultSerializer


class LandingView(NoCSRFView):

    def get(self, request, format=None):
        user = request.user
        courseslist = []
        courses = Course.objects.all().order_by('order')
        faqs = Faq.objects.all()
        results = Result.objects.all()
        for course in courses:
            days = course.expire
            userincourse = UsersInCourse.objects.get(course=course, user=user)
            course_json = CourseSerializer(course).data
            course_json['has_permissions'] = True if user.pk and user in course.users.all() else False
            course_json['expired'] = userincourse.get_expire(days) if userincourse else None
            courseslist.append(course_json)

        return Response(data={
            'courses': courseslist,
            'faqs': FaqSerializer(faqs, many=True).data,
            'results': ResultSerializer(results, many=True).data
        })
