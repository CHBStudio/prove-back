from django.contrib.auth.models import User
from django.db.models import Model
from django.db import models


class Course(Model):
    class Meta:
        verbose_name = 'видео-курс'
        verbose_name_plural = 'видео-курсы'

    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Название')
    description = models.TextField(null=False, blank=False, verbose_name='Описание')
    photo = models.ImageField(upload_to='images', default=None, verbose_name='Фото')
    video = models.FileField(upload_to='video', default=None, verbose_name='Видео')
    video_count = models.IntegerField(null=False, blank=False, verbose_name='Кол-во видео-уроков')
    hour_count = models.IntegerField(null=False, blank=False, verbose_name='Кол-во часов')
    cost = models.IntegerField(null=False, blank=False, verbose_name='Стоимость')
    active = models.BooleanField(default=False, verbose_name='Активный')
    order = models.IntegerField(null=True, blank=True, default=None, verbose_name='Порядок')
    users = models.ManyToManyField(User, verbose_name='Оплатившие')

    def __str__(self):
        return self.title


class Advanteges(Model):
    class Meta:
        verbose_name = 'Плюсы'
        verbose_name_plural = 'Плюсы'

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='advanteges')
    text = models.CharField(max_length=255, blank=False, null=False, verbose_name='Текст')

    def __str__(self):
        return self.text

class Schedule(Model):
    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'расписания'

    DAY_OF_THE_WEEK = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4,'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    )
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='Курс')
    day = models.IntegerField(choices=DAY_OF_THE_WEEK,verbose_name='День')


class Exercise(Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE,related_name='Расписание')
    video = models.FileField(upload_to='private/video/', default=None, verbose_name='Видео')
    description = models.TextField(verbose_name='Описание')
    order = models.IntegerField(blank=True,null=True,verbose_name='Порядок')


