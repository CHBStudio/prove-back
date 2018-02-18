from django.db.models import Model
from django.db import models

class Faq(Model):
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
    question = models.CharField(max_length=255, null=False, blank=False, verbose_name='Вопрос')
    answer = models.TextField(null=False, blank=False, verbose_name='Ответ')

    def __str__(self):
        return self.question

class Result(Model):
    class Meta:
        verbose_name = 'результат'
        verbose_name_plural = 'результаты'
    photo = models.ImageField(upload_to='images',blank=False,null=False,verbose_name='Фото')
    title = models.CharField(max_length=50,blank=False,null=False,default=None,verbose_name='Имя и возраст')
    description = models.TextField(default=None,verbose_name='Описание')

    def __str__(self):
        return 'Photo - {}'.format(self.id)