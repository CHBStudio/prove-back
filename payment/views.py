import hashlib

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from app.decorators import login_required
from app.views import NoCSRFView
from course.models import Course
from prove.settings import MERCHANT_LOGIN, PASSWORD1



