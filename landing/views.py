from rest_framework.response import Response

from app.views import NoCSRFView
from course.models import Course
from course.serializer import CourseSerializer
from landing.models import Faq, Result
from landing.serializer import FaqSerializer, ResultSerializer


class LandingView(NoCSRFView):

    def get(self, request, format=None):
        user = request.user
        courseslist = []
        faqlist = []
        courses = Course.objects.all().order_by('order')
        faqs = Faq.objects.all()
        results = Result.objects.all()
        for result in results:
            result.photo = 'media/' + str(result.photo)
        for course in courses:
            course_json = CourseSerializer(course).data
            course_json['has_permissions'] = True if user.pk and user in course.users.all() else False
            course_json['photo'] = 'media/' + course_json['photo']
            course_json['video'] = 'media/' + course_json['video']
            courseslist.append(course_json)

        return Response(data={
            'courses': courseslist,
            'faqs':FaqSerializer(faqs,many=True).data,
            'results':ResultSerializer(results,many=True).data
        })