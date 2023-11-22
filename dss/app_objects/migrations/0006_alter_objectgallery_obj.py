# Generated by Django 4.2.1 on 2023-11-22 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_objects', '0005_alter_object_call_center_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectgallery',
            name='obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gallery', to='app_objects.object', unique=True, verbose_name='Объект'),
        ),
    ]
