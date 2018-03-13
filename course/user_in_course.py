from datetime import datetime, timedelta

from django.contrib.auth.models import User as CustomUser
from django.db import models
from django.db.models import Model


class UsersInCourse(Model):
    class Meta:
        db_table = "user_in_course"
        verbose_name = 'Оплативший'
        verbose_name_plural = 'Оплатившие'

    course = models.ForeignKey('course.Course', verbose_name="Видео-курс", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь", related_name='users', on_delete=models.CASCADE)
    date = models.DateField(verbose_name=u"Дата оплаты")

    def check_time(self,days):
        delta = datetime.now().date() - self.date
        if delta.days <= days:
            return True

    def get_expire(self,days):
        return round(datetime.timestamp(datetime.combine(self.date + timedelta(days=days), datetime.min.time())))

    def __str__(self):
        return '{} - {}'.format(self.course,self.user)
