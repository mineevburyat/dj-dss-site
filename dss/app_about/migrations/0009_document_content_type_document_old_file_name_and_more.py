# Generated by Django 4.2.1 on 2023-12-03 06:48

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_about', '0008_alter_wp_page_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='content_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='тип скаченного файла'),
        ),
        migrations.AddField(
            model_name='document',
            name='old_file_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='имя скаченного файла'),
        ),
        migrations.AddField(
            model_name='document',
            name='old_url',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='старая ссылка'),
        ),
        migrations.AlterField(
            model_name='wp_page',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='wp_page',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 6, 48, 42, 488234, tzinfo=datetime.timezone.utc), verbose_name='дата создания'),
        ),
    ]