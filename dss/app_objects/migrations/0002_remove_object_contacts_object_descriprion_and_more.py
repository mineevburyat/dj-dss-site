# Generated by Django 4.2.1 on 2023-05-13 08:56

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_objects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='contacts',
        ),
        migrations.AddField(
            model_name='object',
            name='descriprion',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=1000, null=True, verbose_name='краткое описание'),
        ),
        migrations.AddField(
            model_name='object',
            name='slug',
            field=models.SlugField(blank=True, help_text='только латинские буквы и цифры', max_length=15, null=True, unique=True, verbose_name='slug имя в url'),
        ),
        migrations.AlterField(
            model_name='object',
            name='address',
            field=models.CharField(help_text='Адрес по форме город, улица, дом', max_length=200, verbose_name='адрес'),
        ),
    ]
