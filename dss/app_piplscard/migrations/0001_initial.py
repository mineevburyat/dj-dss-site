# Generated by Django 4.2.1 on 2023-11-20 13:39

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_mediafiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Piple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=120, verbose_name='полное имя')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(max_length=650, verbose_name='краткое описание')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_mediafiles.image', verbose_name='фото')),
            ],
            options={
                'verbose_name': 'сотрудник',
                'verbose_name_plural': 'сотрудники',
            },
        ),
    ]
