# Generated by Django 4.1.4 on 2022-12-28 10:11

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportdss', '0015_rename_name_email_email_rename_name_phone_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingmode',
            name='mode',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=300, verbose_name='режим работы'),
        ),
    ]
