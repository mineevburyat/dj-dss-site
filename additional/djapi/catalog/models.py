from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Genre(models.Model):
    """\
    Модель отображает жанр книги (Фантастика, Классика, Научпоп и пр.)
    """
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    name = models.CharField(
        "Имя жанра",
        max_length=200, 
        help_text="Укажите жанр книги (такие как Научная фантастика, французкая поэзия и пр.)"
    )

    def __str__(self):
        """
        Строковое предстваление жанра
        """
        return self.name

class Language(models.Model):
    """\
        Языки используемые в библиотеке"""
    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"
    name = models.CharField(
        "название языка",
        max_length=100,
        help_text="название языка"
    )    
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Модель книги
    """
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        # ordering = ['title', 'author']

    title = models.CharField(
        "Название книги",
        max_length=200
    )
    author = models.ForeignKey(
        'Author', 
        on_delete=models.SET_NULL, 
        null=True
    )
    summary = models.TextField(
        max_length=1000, 
        help_text="Введите краткое описание книги"
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13, 
        help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    genre = models.ManyToManyField(
        Genre, 
        help_text="Выберите жанры для этой книги"
    )
    language = models.ForeignKey(
        Language,
        help_text="выберите язык на котором написана книга",
        on_delete=models.SET_NULL,
        null=True
    ) 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        # return reverse('book_detail', args=[self.id])
        return f'{self.id}'
    
    def display_genre(self):
        """
        Создать строку перечисления жанров. 
        Это требуется для отображения жанров книги в админке
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Жанр'

class BookInstance(models.Model):
    """
    Модель реальной книги имеющей идентификатор или штрих-код
    """
    class Meta:
        verbose_name = "Экземпляр в библиотеке"
        verbose_name_plural = "Экземпляры в библиотеке"
        ordering = ["due_back"]

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text="уникальный индентификатор этой книги в библиотеке"
    )
    book = models.ForeignKey(
        'Book', 
        on_delete=models.SET_NULL, 
        null=True
    )
    imprint = models.CharField(
        "издательство",
        max_length=200
    )
    due_back = models.DateField(
        'Дата возврата',
        null=True, 
        blank=True
    )
    LOAN_STATUS = (
        ('m', 'на техобслуживании'),
        ('o', 'на руках'),
        ('a', 'доступен'),
        ('r', 'зарезервирован'),
    )
    status = models.CharField(
        "статус",
        max_length=1, 
        choices=LOAN_STATUS, 
        blank=True, 
        default='m', 
        help_text='выберите статус книги'
    )

    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)

class Author(models.Model):
    """
    Модель представляющая автора 
    (учитывая западные стили и восточные стили имен)
    """
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = []
        # label = 'Автор'
    
    NAME_STYLE = (
        ('lt', 'латинский'),
        ('ru', 'славянский'),
        ('ch', 'азиатско-китайский'),
        ('ar', 'арабский'),
        ('tr', 'тюрко и монгольский')
    )

    last_name = models.CharField(
        'Фамилия (насаб)',
        max_length=100,
        help_text="имя семейное (фамилия или ряд ибн для арабоговорящих) "
    )
    first_name = models.CharField(
        'Имя (алам)',
        max_length=100,
        help_text="имя данное при рождении"
    )
    middle_name = models.CharField(
        'Второе имя (среднее, прозвище, псевдоним))',
        max_length=100,
        blank=True,
        help_text="религиозное имя или титул, прозвище, достижение для арабоговорящих"
    )
    patronymic = models.CharField(
        'Отчество (нисба)',
        max_length=100,
        blank=True,
        help_text="склоняемое имя отца для восточнославянских народов, не склоняемое имя отца для тюркоговорящих народов или место рождения, религиозная принадлежность для арабоговорящих"
    )
    style_name = models.CharField(
        "стиль написания имени",
        max_length=2, 
        choices=NAME_STYLE, 
        blank=True, 
        default='ru', 
        help_text='выберите стиль написания полного имени автора'
    )
    date_of_birth = models.DateField(
        "дата рождения",
        null=True, 
        blank=True
    )
    date_of_death = models.DateField(
        'дата смерти', 
        null=True, 
        blank=True
    )

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def get_full_name(self):
        """
        Строка представления полного имени автора
        """
        if self.style_name == "lt":
            # латинизированный стиль
            # индивидуальноеимя среднееимя последнееимя
            return f'{self.first_name} {self.middle_name} {self.last_name}'
        elif self.style_name == "ru":
            # славянский стиль
            # фамилия индивидуальноеимя отчество
            return f'{self.last_name} {self.first_name} {self.patronymic}'
        elif self.style_name == "ch":
            # китайский стиль
            # фамилия имя
            return f'{self.last_name} {self.first_name}'
        elif self.style_name == "tr":
            # монгольский стиль
            # имя-имяотца фамилия
            return f'{self.first_name}-{self.patronymic} {self.last_name}'
        else:
            return f'{self.first_name} {self.middle_name} {self.last_name}'
    get_full_name.short_description = "полное имя"
    def __str__(self):
        return self.get_full_name()