from django.contrib.auth.models import User
from django.db.models import Model
from django.db import models

from course.user_in_course import UsersInCourse


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
    old_cost = models.IntegerField(null=True, blank=True, verbose_name='Стоимость без скидки')
    cost = models.IntegerField(null=False, blank=False, verbose_name='Стоимость(финальная)')
    active = models.BooleanField(default=False, verbose_name='Активный')
    order = models.IntegerField(null=True, blank=True, default=None, verbose_name='Порядок')
    users = models.ManyToManyField(User, through=UsersInCourse, verbose_name='Оплатившие')
    expire = models.IntegerField(default=40, verbose_name='Период действия(в днях)')
    food = models.TextField(default='Default', verbose_name='Питание')
    extra = models.TextField(default='Default', verbose_name='Прочее')

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
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    day = models.IntegerField(choices=DAY_OF_THE_WEEK, verbose_name='День')
    week = models.IntegerField(verbose_name='Номер недели')


class Exercise(Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='Расписание')
    title = models.CharField(max_length=255, blank=False, null=False, default='default', verbose_name='Заголовок')
    video = models.FileField(upload_to='private/video/', default=None, verbose_name='Видео')
    description = models.TextField(verbose_name='Описание')
    order = models.IntegerField(blank=True, null=True, verbose_name='Порядок')
