# Generated by Django 2.0.2 on 2018-02-18 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_auto_20180218_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(default=None, upload_to='video/exercise', verbose_name='Видео')),
                ('description', models.TextField(verbose_name='Описание')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Порядок')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[('1', 'Понедельник'), ('2', 'Вторник'), ('3', 'Среда'), ('4', 'Четверг'), ('5', 'Пятница'), ('6', 'Суббота'), ('7', 'Воскресенье')])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Курс', to='course.Course')),
            ],
            options={
                'verbose_name': 'расписание',
                'verbose_name_plural': 'расписания',
            },
        ),
        migrations.AddField(
            model_name='exercise',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Расписание', to='course.Schedule'),
        ),
    ]
