from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from app.decorators import login_required
from app.middleware import CsrfExemptSessionAuthentication
from course.models import Course
from course.serializer import CourseSerializer


class NoCSRFView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)



