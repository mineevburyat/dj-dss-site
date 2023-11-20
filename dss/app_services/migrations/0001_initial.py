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
            name='TypeService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=60, unique=True, verbose_name='Название группы услуг')),
                ('slug', models.CharField(db_index=True, max_length=60, unique=True, verbose_name='название на английском')),
                ('order', models.SmallIntegerField(default=255, verbose_name='сортировка')),
                ('category', models.CharField(choices=[('sport', 'Спортивные услуги'), ('section', 'Спортивные секции'), ('relax', 'Отдых'), ('other', 'Прочие услуги')], default='other', max_length=10, verbose_name='категория услуги')),
                ('description', models.TextField(default='необходимо заполнить', help_text='кратко описываем группу услуг', max_length=800, verbose_name='Описание группы услуг')),
                ('active', models.BooleanField(default=True, verbose_name='активно')),
                ('icon', models.ForeignKey(default=14, on_delete=django.db.models.deletion.PROTECT, to='app_mediafiles.icon', verbose_name='иконка')),
            ],
            options={
                'verbose_name': 'Тип услуги',
                'verbose_name_plural': 'Типы услуг',
            },
        ),
        migrations.CreateModel(
            name='TypeServiceGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='service', to='app_mediafiles.image', verbose_name='фотографии')),
                ('typeservice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='photo', to='app_services.typeservice', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Фотография вида услуг',
                'verbose_name_plural': 'Галерея фотографий услуг',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='название услуги')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(max_length=2500, verbose_name='краткое описание')),
                ('category', models.CharField(choices=[('sport', 'Спортивные услуги'), ('section', 'Спортивные секции'), ('relax', 'Отдых'), ('other', 'Прочие услуги')], max_length=10, verbose_name='категория услуги')),
                ('slug', models.SlugField(blank=True, help_text='только латинские буквы и цифры', max_length=120, null=True, unique=True, verbose_name='slug имя в url')),
                ('order', models.IntegerField(default=100, verbose_name='важность')),
                ('typeservice', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app_services.typeservice', verbose_name='группа услуг')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('forchild', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicerate', to='app_services.service', verbose_name='услуга')),
            ],
            options={
                'verbose_name': 'тариф',
                'verbose_name_plural': 'тарифы',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('start_date', 'end_date')},
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('pct', 'Скидка в %'), ('amt', 'Фиксированная стоимость')], max_length=3)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='app_services.rate')),
            ],
            options={
                'verbose_name': 'дисконт',
                'verbose_name_plural': 'дисконты',
            },
        ),
    ]
