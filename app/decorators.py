from rest_framework.exceptions import PermissionDenied


def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.pk:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap