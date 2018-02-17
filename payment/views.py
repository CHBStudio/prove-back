import hashlib

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from app.decorators import login_required
from app.views import NoCSRFView
from prove.settings import MERCHANT_LOGIN, PASSWORD1


class UrlView(NoCSRFView):

    @method_decorator(login_required)
    def get(self, request):
        SignatureValue = hashlib.md5(
            '{}:{}:{}:{}'.format(MERCHANT_LOGIN, '3000.00', request.user.id, PASSWORD1).encode('utf-8')).hexdigest()
        url = 'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={}&OutSum={}&InvId={}&SignatureValue={}&IsTest=1'.format(
            MERCHANT_LOGIN, '3000.00', request.user.id, SignatureValue)

        return Response(data={
            'url': url
        })
