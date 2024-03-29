# Generated by Django 4.2.1 on 2023-11-22 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_objects', '0004_remove_sportareagallery_photos_and_more'),
        ('app_contacts', '0003_phone_name_alter_phone_phone_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='sportarea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='area_contact', to='app_objects.sportarea', verbose_name='спортплощадка'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='phone_url',
            field=models.CharField(default='+7', help_text='согласно e164 (ссылка)', max_length=16, verbose_name='url'),
        ),
    ]
