from django.contrib import admin

# Register your models here.
# from .models import Author, Genre, Book, BookInstance, Language
# '''\
#     три способа регистрации администрирования модели:
#     1. простая регистрация
#     2. регистрация с настраивающимся классом
#     3. регистрация настраивающего клсса с помощью декоратора'''

# # admin.site.register(BookInstance)
# class BooksInstanceInline(admin.TabularInline):
#     model = BookInstance
#     extra = 0
# @admin.register(BookInstance)
# class BookInstanceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'imprint', 'status', 'due_back')
#     list_filter = ('status', 'due_back')
#     fieldsets = (
#         (None, {
#             'fields': ('book','imprint', 'id')
#         }),
#         ('Availability', {
#             'fields': ('status', 'due_back')
#         }),
#     )

# # admin.site.register(Author)
# class BookInline(admin.TabularInline):
#     model = Book
#     extra = 0

# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('get_full_name', 'date_of_birth', 'date_of_death')
#     fields = [('first_name', 'last_name', 'patronymic', 'middle_name'), ('date_of_birth', 'date_of_death')]
#     inlines = [BookInline]
# admin.site.register(Author, AuthorAdmin)

# # admin.site.register(Book)
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'display_genre', 'language')
#     inlines = [BooksInstanceInline]



# # admin.site.register(Genre)
# @admin.register(Genre)
# class GenreAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Language)
# class LanguageAdmin(admin.ModelAdmin):
#     pass