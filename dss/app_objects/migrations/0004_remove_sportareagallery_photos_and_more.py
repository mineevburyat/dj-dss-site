# Generated by Django 4.2.1 on 2023-11-21 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_mediafiles', '0002_alter_image_date_public'),
        ('app_objects', '0003_remove_objectgallery_photos_objectgallery_photos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportareagallery',
            name='photos',
        ),
        migrations.AddField(
            model_name='sportareagallery',
            name='photos',
            field=models.ManyToManyField(to='app_mediafiles.image', verbose_name='фотографии'),
        ),
    ]
