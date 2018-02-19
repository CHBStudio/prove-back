import hashlib
from datetime import datetime

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from app.decorators import login_required
from app.views import NoCSRFView
from course.models import Course
from payment.models import Payment
from prove.settings import MERCHANT_LOGIN, PASSWORD1, PASSWORD2


class PaymentView(NoCSRFView):

    def get(self, request):
        outsum = request.GET.get('OutSum')
        user_id = request.GET.get('InvId')
        signature = request.GET.get('SignatureValue')
        course_id = request.GET.get('Shp_course')
        try:
            course = Course.objects.get(id=course_id)
            user = User.objects.get(id=user_id)
        except:
            course = None
            user=None
        SignatureValue = hashlib.md5(
            '{}:{}:{}:{}:Shp_course={}'.format(MERCHANT_LOGIN, outsum, user_id, PASSWORD2, course_id).encode(
                'utf-8')).hexdigest()
        if signature == SignatureValue:
            Payment(
                user_id=user_id,
                money=int(outsum),
                create_at=datetime.now(),
                course_id=int(course_id)
            ).save()
            course.users.add(user)
            course.save()

        return Response(
            data='OK{}'.format(user_id)
        )

