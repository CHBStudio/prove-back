# Generated by Django 2.0.2 on 2018-02-22 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0017_schedule_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='week',
            name='course',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='week',
            field=models.IntegerField(verbose_name='Номер недели'),
        ),
        migrations.DeleteModel(
            name='Week',
        ),
    ]