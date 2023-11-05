# Generated by Django 4.2.1 on 2023-11-04 04:32

import app_booking.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app_objects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubunitBooking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "checkin_date",
                    models.DateField(
                        default=datetime.datetime.now, verbose_name="дата бронирования"
                    ),
                ),
                (
                    "time_slot",
                    models.JSONField(
                        default=app_booking.models.json_default_value,
                        verbose_name="время начала и конца бронирования",
                    ),
                ),
                (
                    "subunit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="app_objects.subunit",
                        verbose_name="ресурс",
                    ),
                ),
            ],
            options={
                "verbose_name": "бронирование ресурса",
                "verbose_name_plural": "забронированные ресурсы",
            },
        ),
    ]
