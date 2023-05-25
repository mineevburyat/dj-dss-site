# Generated by Django 4.2.1 on 2023-05-24 13:13

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_piplscard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='piple',
            options={'verbose_name': 'сотрудник', 'verbose_name_plural': 'сотрудники'},
        ),
        migrations.AlterField(
            model_name='piple',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=650, verbose_name='краткое описание'),
        ),
    ]