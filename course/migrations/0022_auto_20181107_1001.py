# Generated by Django 2.0.2 on 2018-11-07 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_course_expire'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='old_cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='Стоимость со скидкой'),
        ),
        migrations.AlterField(
            model_name='course',
            name='cost',
            field=models.IntegerField(verbose_name='Стоимость без скидки'),
        ),
    ]
