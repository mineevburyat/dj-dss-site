# Generated by Django 4.2.1 on 2023-11-22 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_objects', '0005_alter_object_call_center_and_more'),
        ('app_contacts', '0006_remove_contact_name_alter_contact_sportarea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='sportarea',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='contact_area', to='app_objects.sportarea', verbose_name='спортплощадка'),
        ),
    ]
