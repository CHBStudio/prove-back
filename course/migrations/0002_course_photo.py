# Generated by Django 2.0.2 on 2018-02-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='photo',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='media/'),
        ),
    ]
