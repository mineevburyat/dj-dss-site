# Generated by Django 4.2.1 on 2023-05-24 14:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_objects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubunitBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_date', models.DateField(default=datetime.datetime.now, verbose_name='дата бронирования')),
                ('time_slot', models.JSONField(verbose_name='время начала и конца бронирования')),
                ('subunit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_objects.subunit', verbose_name='ресурс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'бронирование ресурса',
                'verbose_name_plural': '',
            },
        ),
    ]