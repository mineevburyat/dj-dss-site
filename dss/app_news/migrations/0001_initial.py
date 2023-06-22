# Generated by Django 4.2.1 on 2023-06-18 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ImageMedia",
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
                    "slug",
                    models.SlugField(
                        max_length=120, unique=True, verbose_name="часть url"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        db_index=True, max_length=120, verbose_name="название"
                    ),
                ),
                (
                    "caption",
                    models.TextField(
                        db_index=True, max_length=500, verbose_name="подпись к картинке"
                    ),
                ),
                (
                    "alt_txt",
                    models.CharField(
                        max_length=160, verbose_name="альтернативная подпись"
                    ),
                ),
                (
                    "date_public",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="время добавления"
                    ),
                ),
                (
                    "img_file_size",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="объем файла"
                    ),
                ),
                (
                    "img_mode",
                    models.CharField(
                        blank=True,
                        help_text="color, grey, and other",
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "width",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="ширина в пикселях"
                    ),
                ),
                (
                    "height",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="высота в пикселях"
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="media_image", verbose_name="картинка"),
                ),
                (
                    "media_type",
                    models.CharField(
                        blank=True,
                        help_text="расширение файла",
                        max_length=5,
                        null=True,
                        verbose_name="расширение",
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media_image/thumbnail",
                        verbose_name="width 150",
                    ),
                ),
                (
                    "medium",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media_image/medium",
                        verbose_name="with 320",
                    ),
                ),
                (
                    "large",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media_image/large",
                        verbose_name="with 1080",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
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
                ("slug", models.SlugField(max_length=100)),
                ("date_public", models.DateTimeField(verbose_name="дата публикации")),
                ("title", models.CharField(max_length=100, verbose_name="заголовок")),
                (
                    "excerpt",
                    models.TextField(
                        blank=True, max_length=250, null=True, verbose_name="отрывок"
                    ),
                ),
                (
                    "content",
                    models.TextField(max_length=2000, verbose_name="содержание"),
                ),
                (
                    "featured_media",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app_news.imagemedia",
                        verbose_name="id media",
                    ),
                ),
            ],
            options={"verbose_name": "новость",},
        ),
    ]