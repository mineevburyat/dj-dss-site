# Generated by Django 4.2.1 on 2023-08-17 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_objects', '0002_object_call_center'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='type_stock',
        ),
        migrations.AddField(
            model_name='typestock',
            name='obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='obj', to='app_objects.object', verbose_name='Объект'),
        ),
    ]
