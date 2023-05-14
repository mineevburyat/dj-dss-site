# Generated by Django 4.2.1 on 2023-05-14 05:27

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_objects', '0005_object_icon_object_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subunit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='подразделение, отдел, направление', max_length=25, verbose_name='название направления')),
                ('slug', models.SlugField(help_text='только латинские буквы и цифры', max_length=25, unique=True, verbose_name='slug имя в url')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=1000, null=True, verbose_name='Описание подразделения, характеристики')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='objects', verbose_name='пиктограмка')),
                ('photo', models.ImageField(blank=True, help_text='в будущем набор фотографий для слайдера', null=True, upload_to='objects', verbose_name='фотография подразделения')),
                ('contact', models.CharField(help_text='по сути объект с названием типом связи и пр. возможно несколько', max_length=25, verbose_name='Телефон')),
                ('shedule', models.CharField(help_text='режим работы, график, сан. день (как календарь)', max_length=25, verbose_name='график работы')),
            ],
        ),
        migrations.AddField(
            model_name='object',
            name='subunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_objects.subunit', verbose_name='Подразделение'),
        ),
    ]