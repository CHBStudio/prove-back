# Generated by Django 2.0.2 on 2018-02-22 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_exercise_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(verbose_name='Номер недели')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'неделя',
                'verbose_name_plural': 'недели',
            },
        ),
        migrations.AlterField(
            model_name='schedule',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='Курс'),
        ),
    ]