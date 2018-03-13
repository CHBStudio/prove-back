# Generated by Django 2.0.2 on 2018-03-13 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0018_auto_20180222_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersInCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата оплаты')),
            ],
            options={
                'db_table': 'user_in_course',
                'verbose_name_plural': 'Оплатившие',
                'verbose_name': 'Оплативший',
            },
        ),
        migrations.RemoveField(
            model_name='course',
            name='users',
        ),
        migrations.AddField(
            model_name='usersincourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='Видео-курс'),
        ),
        migrations.AddField(
            model_name='usersincourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
