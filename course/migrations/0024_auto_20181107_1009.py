# Generated by Django 2.0.2 on 2018-11-07 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0023_auto_20181107_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='cost_discount',
        ),
        migrations.AddField(
            model_name='course',
            name='old_cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='Стоимость без скидки'),
        ),
        migrations.AlterField(
            model_name='course',
            name='cost',
            field=models.IntegerField(verbose_name='Стоимость(финальная)'),
        ),
    ]
