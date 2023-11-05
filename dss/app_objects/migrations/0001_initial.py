# Generated by Django 4.2.1 on 2023-11-04 04:32

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app_mediafiles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Object",
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
                    "short_name",
                    models.CharField(
                        help_text="Короткое имя объекта (не более 20 символов)",
                        max_length=20,
                        verbose_name="краткое имя",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Полное официальное имя (не более 250  символов)",
                        max_length=250,
                        verbose_name="официальное имя",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="только латинские буквы и цифры",
                        max_length=20,
                        unique=True,
                        verbose_name="slug имя в url",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        help_text="Адрес по форме город, улица, дом",
                        max_length=200,
                        verbose_name="адрес",
                    ),
                ),
                (
                    "description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True,
                        max_length=3000,
                        null=True,
                        verbose_name="краткое описание",
                    ),
                ),
                (
                    "order",
                    models.SmallIntegerField(default=100, verbose_name="Сортировка"),
                ),
                (
                    "start_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="дата ввода в эксплуатацию"
                    ),
                ),
                (
                    "square",
                    models.CharField(
                        default="-", max_length=11, verbose_name="площадь"
                    ),
                ),
                (
                    "call_center",
                    models.CharField(
                        default="+7(3012) 5-30-36",
                        max_length=20,
                        verbose_name="номер телефона",
                    ),
                ),
                (
                    "icon_lib",
                    models.ForeignKey(
                        default=14,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="app_mediafiles.icon",
                        verbose_name="иконка",
                    ),
                ),
            ],
            options={"verbose_name": "Объект", "verbose_name_plural": "Объекты",},
        ),
        migrations.CreateModel(
            name="SportArea",
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
                    "name",
                    models.CharField(
                        help_text="бассейн, стадион, тренажерный зал, универсальный зал и пр.",
                        max_length=35,
                        verbose_name="название",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="желательно английское название",
                        max_length=25,
                        unique=True,
                        verbose_name="slug имя в url",
                    ),
                ),
                ("order", models.IntegerField(default=100, verbose_name="сортировка")),
                (
                    "description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        default="",
                        help_text="описание спортплощадки без характеристик и расписания",
                        max_length=1500,
                        verbose_name="краткое описание",
                    ),
                ),
                (
                    "inviting_mes",
                    models.TextField(
                        default="призывной призыв или слоган",
                        max_length=90,
                        verbose_name="слоган или призыв к посещению",
                    ),
                ),
                (
                    "characteristics",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="характеристики спортплощадки",
                    ),
                ),
                (
                    "icon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="app_mediafiles.icon",
                        verbose_name="файл иконки",
                    ),
                ),
                (
                    "obj",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sportarea",
                        to="app_objects.object",
                        verbose_name="Объект",
                    ),
                ),
            ],
            options={
                "verbose_name": "спортплощадка",
                "verbose_name_plural": "спортплощадки",
            },
        ),
        migrations.CreateModel(
            name="Subunit",
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
                    "name",
                    models.CharField(
                        help_text="дрожка бассейна №1, мини-поле №2",
                        max_length=45,
                        verbose_name="название конкретного ресурса",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="только латинские буквы и цифры",
                        max_length=45,
                        unique=True,
                        verbose_name="slug имя в url",
                    ),
                ),
                (
                    "description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True,
                        max_length=1000,
                        null=True,
                        verbose_name="Описание ресурса, характеристики",
                    ),
                ),
                (
                    "contact",
                    models.CharField(
                        blank=True,
                        help_text="ссылки на контакт TODO",
                        max_length=25,
                        null=True,
                        verbose_name="Телефон",
                    ),
                ),
                (
                    "shedule",
                    models.CharField(
                        blank=True,
                        help_text="режим работы, график, сан. день (как календарь)",
                        max_length=25,
                        null=True,
                        verbose_name="график работы",
                    ),
                ),
                (
                    "obj",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="app_objects.object",
                        verbose_name="Объект",
                    ),
                ),
                (
                    "resource",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="app_objects.sportarea",
                        verbose_name="тип ресурса",
                    ),
                ),
            ],
            options={"verbose_name": "Ресурс", "verbose_name_plural": "Ресурсы",},
        ),
        migrations.CreateModel(
            name="ObjectGallery",
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
                    "obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="gallery",
                        to="app_objects.object",
                        verbose_name="Объект",
                    ),
                ),
                (
                    "photos",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="app_mediafiles.image",
                        verbose_name="фотографии",
                    ),
                ),
            ],
            options={
                "verbose_name": "Галерея фотографий объекта",
                "verbose_name_plural": "Галереи фотографий объектов",
            },
        ),
    ]
