# Generated by Django 4.2.1 on 2023-11-14 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_services", "0007_alter_discount_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="service", name="object",),
        migrations.RemoveField(model_name="service", name="sportarea",),
        migrations.AddField(
            model_name="rate",
            name="forchild",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="rate",
            name="service",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="servicerate",
                to="app_services.service",
                verbose_name="услуга",
            ),
        ),
    ]