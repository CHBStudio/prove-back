from django.contrib import admin
from django.contrib.admin import AdminSite

from course.models import Course, Advanteges


class ProveAdminSite(AdminSite):
    site_header = 'Prove Project'
    site_url = None


prove = ProveAdminSite()
admin.autodiscover()
