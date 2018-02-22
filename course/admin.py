from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin, TabularInline
from django.contrib.auth.models import User

from course.models import Course, Advanteges, Exercise, Schedule


class AdvantegesInline(TabularInline):
    model = Advanteges
    extra = 0

class UsersInline(TabularInline):
    model = Course.users.through
    extra = 0


class ExerciseInline(TabularInline):
    model = Exercise
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_count', 'hour_count', 'photo', 'video', 'cost', 'active', 'description', 'order')
    fields = ('title', 'video_count', 'hour_count', 'photo', 'video', 'cost', 'active', 'description', 'order','food','extra')
    list_filter = ('order', 'cost')
    inlines = (AdvantegesInline,UsersInline)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'day')
    fields = ('course', 'day')
    list_filter = ('course','day')
    inlines = (ExerciseInline,)

admin.site.register(Course, CourseAdmin)
admin.site.register(Schedule,ScheduleAdmin)