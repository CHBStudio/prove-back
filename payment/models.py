from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model

from course.models import Course


class Payment(Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Пользователь')
    money = models.IntegerField(verbose_name='Сумма')
    create_at = models.DateTimeField(verbose_name='Дата оплаты')
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,blank=True)