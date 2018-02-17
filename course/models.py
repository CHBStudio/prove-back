from django.contrib.auth.models import User
from django.db.models import Model
from django.db import models


class Course(Model):
    class Meta:
        verbose_name = 'видео-курс'
        verbose_name_plural = 'видео-курсы'

    title = models.CharField(max_length=255, null=False, blank=False,verbose_name='Название')
    description = models.TextField(null=False,blank=False,verbose_name='Описание')
    photo = models.ImageField(upload_to = 'media/images', default = None,verbose_name='Фото')
    video = models.FileField(upload_to='media/video', default = None, verbose_name='Видео')
    video_count = models.IntegerField(null=False,blank=False,verbose_name='Кол-во видео-уроков')
    hour_count = models.IntegerField(null=False,blank=False,verbose_name='Кол-во часов')
    cost = models.IntegerField(null=False,blank=False,verbose_name='Стоимость')
    active = models.BooleanField(default=False,verbose_name='Активный')
    order = models.IntegerField(null=True,blank=True,default=None,verbose_name='Порядок')
    users = models.ManyToManyField(User,verbose_name='Оплатившие')

class Advanteges(Model):
    class Meta:
        verbose_name = 'Плюсы'
        verbose_name_plural = 'Плюсы'

    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='advanteges')
    text = models.CharField(max_length=255,blank=False,null=False,verbose_name='Текст')

    def __str__(self):
        return self.text

