# Generated by Django 2.0.2 on 2018-02-22 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0016_auto_20180222_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='week',
            field=models.ForeignKey(default=1, on_delete='CASCADE', to='course.Week', verbose_name='Неделя'),
        ),
    ]