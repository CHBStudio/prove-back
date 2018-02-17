from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin, TabularInline
from django.contrib.auth.models import User

from app.admin import prove
from course.models import Course, Advanteges


class AdvantegesInline(TabularInline):
    model = Advanteges
    extra = 0

class UsersInline(TabularInline):
    model = Course.users.through
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_count', 'hour_count', 'photo', 'video', 'cost', 'active', 'description', 'order')
    fields = ('title', 'video_count', 'hour_count', 'photo', 'video', 'cost', 'active', 'description', 'order')
    list_filter = ('order', 'cost')
    inlines = (AdvantegesInline,UsersInline)


admin.site.register(Course, CourseAdmin)
prove.register(Advanteges)
